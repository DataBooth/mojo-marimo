"""Execute Mojo code with binary caching for fast repeated execution.

The executor compiles Mojo code once and caches the binary, making subsequent
executions much faster (~10-50ms vs ~1-2s).
"""

import hashlib
import subprocess
import tempfile
from functools import cache
from pathlib import Path
from textwrap import dedent

from py_run_mojo.validator import get_validation_hint, validate_mojo_code

# Cache directory for compiled Mojo binaries
CACHE_DIR = Path.home() / ".mojo_cache" / "binaries"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


@cache
def get_mojo_version() -> str:
    """Get the installed Mojo version.

    Preference order:
    1. The Python ``mojo`` package's version (if importable).
    2. The ``mojo --version`` CLI output (if it looks like a Modular CLI).

    Both paths are defensive: if anything looks wrong we return ``"Unknown"``
    rather than surfacing raw shell errors in user-facing UIs.
    """

    # 1. Try the Python package first; this avoids PATH/shim issues and is
    # usually present whenever Mojo is installed via Modular's tooling.
    try:  # pragma: no cover - import shape may vary across versions
        import mojo  # type: ignore[import]

        pkg_version = getattr(mojo, "__version__", None) or getattr(mojo, "version", None)
        if isinstance(pkg_version, str) and pkg_version.strip():
            # Normalise to the same shape the CLI uses for easier display.
            if pkg_version.startswith("Mojo "):
                return pkg_version.strip()
            return f"Mojo {pkg_version.strip()}"
    except Exception:
        # Fall back to CLI discovery below.
        pass

    # 2. Fallback: shell out to the CLI, but only trust sane output.
    try:
        result = subprocess.run(
            ["mojo", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return "Unknown"

    stdout = (result.stdout or "").strip()

    # Non-zero exit or obviously wrong output – treat as unavailable.
    if result.returncode != 0:
        return "Unknown"

    if not stdout or not stdout.startswith("Mojo "):
        return "Unknown"

    return stdout


def run_mojo(
    source: str,
    echo_code: bool = False,
    echo_output: bool = False,
    use_cache: bool = True,
    extra_args: list[str] | None = None,
) -> str | None:
    """Execute Mojo code with optional binary caching.

    Args:
        source: Mojo code string or file path.
        echo_code: Print the code before running.
        echo_output: Print the output after running.
        use_cache: Use cached binaries for faster repeated execution (default True).
                   Set to False to always recompile.
        extra_args: Optional list of extra arguments.

    Returns:
        The stdout output if successful, else None.

    Example:
        >>> code = '''\n        ... fn main():\n        ...     print("Hello from Mojo!")\n        ... '''\n        >>> output = run_mojo(code)
        >>> print(output)
        Hello from Mojo!
    """
    if not source.strip():
        print("Error: Empty source provided.")
        return None

    path = Path(source)
    mojo_code: str

    # Read or use source code
    if path.is_file():
        try:
            mojo_code = path.read_text()
        except OSError as e:
            print(f"Error reading file {path}: {e}")
            return None
        if echo_code:
            print(f"### Mojo code from file: {path}\n")
    else:
        # Auto-dedent inline Mojo code to handle indented triple-quoted strings
        mojo_code = dedent(source)
        if echo_code:
            print("### Mojo code from string\n")

    if echo_code:
        print(mojo_code)
        print("-" * 80)

    # Validate Mojo code before compilation
    is_valid, error_msg = validate_mojo_code(mojo_code)
    if not is_valid:
        print(f"### Validation Error: {error_msg}")
        hint = get_validation_hint(error_msg)
        if hint:
            print(hint)
        return None

    # Generate cache key from source code hash
    code_hash = hashlib.sha256(mojo_code.encode("utf-8")).hexdigest()[:16]
    cache_key = f"mojo_{code_hash}"
    cached_binary = CACHE_DIR / cache_key

    # Compile if not cached
    if not use_cache or not cached_binary.exists():
        if use_cache and echo_output:
            print(f"[Compiling and caching as {cache_key}...]")

        # Write source to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".mojo", delete=False) as tmp:
            tmp.write(mojo_code)
            source_file = tmp.name

        try:
            # Compile to binary
            compile_cmd = ["mojo", "build", source_file, "-o", str(cached_binary)]
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if compile_result.returncode != 0:
                print(f"### Compilation failed:\n{compile_result.stderr}")
                return None

        finally:
            Path(source_file).unlink(missing_ok=True)

    elif echo_output:
        print(f"[Using cached binary {cache_key}]")

    # Run the cached binary
    run_cmd = [str(cached_binary)]
    if extra_args:
        run_cmd.extend(extra_args)

    try:
        result = subprocess.run(
            run_cmd,
            capture_output=True,
            text=True,
            check=False,
        )

        output: str | None = None
        if result.stdout:
            output = result.stdout.strip()
            if echo_output:
                print(f"\n### Output - {get_mojo_version()}:\n{output}")

        if result.stderr:
            print(f"\n### Runtime errors:\n{result.stderr}")

        if result.returncode != 0:
            return None

        return output

    except subprocess.SubprocessError as e:
        print(f"Subprocess error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def clear_cache():
    """Clear all cached Mojo binaries."""
    import shutil

    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Cache cleared: {CACHE_DIR}")
    else:
        print("Cache directory doesn't exist")


def cache_stats():
    """Show cache statistics."""
    if not CACHE_DIR.exists():
        print("Cache directory doesn't exist")
        return

    binaries = list(CACHE_DIR.glob("mojo_*"))
    total_size = sum(b.stat().st_size for b in binaries)

    print(f"Cache directory: {CACHE_DIR}")
    print(f"Cached binaries: {len(binaries)}")
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    print(f"Mojo version: {get_mojo_version()}\n")

    # Example: Direct code execution
    print("=== Example: Running Mojo code ===")
    code = """
fn main():
    print("Hello from Mojo!")
"""
    result = run_mojo(code, echo_output=True)

    # Example: With caching disabled
    print("\n=== Example: Running without cache ===")
    result = run_mojo(code, echo_output=True, use_cache=False)

    print("\nFor more examples, see examples.py")
    print()
    cache_stats()
