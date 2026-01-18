"""Cached execution of Mojo code via compiled binaries.

This adds a caching layer to mo_run_mojo that compiles code once
and reuses the binary on subsequent calls.
"""

from functools import cache
from pathlib import Path
from typing import Optional
import subprocess
import tempfile
import hashlib


# Cache directory for compiled Mojo binaries
CACHE_DIR = Path.home() / ".mojo_cache" / "binaries"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


@cache
def get_mojo_version() -> str:
    """Get the installed Mojo version."""
    try:
        return subprocess.getoutput("mojo --version").strip()
    except Exception:
        return "Unknown"


def mo_run_mojo_cached(
    source: str,
    echo_code: bool = False,
    echo_output: bool = False,
    use_cache: bool = True,
    extra_args: Optional[list[str]] = None,
) -> Optional[str]:
    """
    Run Mojo code with binary caching.
    
    First call: compiles and caches the binary.
    Subsequent calls: runs cached binary directly (much faster).
    
    Args:
        source: Mojo code string or file path.
        echo_code: Print the code before running.
        echo_output: Print the output after running.
        use_cache: Use cached binaries (default True).
        extra_args: Optional list of extra arguments.
    
    Returns:
        The stdout output if successful, else None.
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
        mojo_code = source
        if echo_code:
            print("### Mojo code from string\n")
    
    if echo_code:
        print(mojo_code)
        print("-" * 80)
    
    # Generate cache key from source code hash
    code_hash = hashlib.sha256(mojo_code.encode('utf-8')).hexdigest()[:16]
    cache_key = f"mojo_{code_hash}"
    cached_binary = CACHE_DIR / cache_key
    
    # Compile if not cached
    if not use_cache or not cached_binary.exists():
        if use_cache and echo_output:
            print(f"[Compiling and caching as {cache_key}...]")
        
        # Write source to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mojo', delete=False) as tmp:
            tmp.write(mojo_code)
            source_file = tmp.name
        
        try:
            # Compile to binary
            compile_cmd = ['mojo', 'build', source_file, '-o', str(cached_binary)]
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
        
        output: Optional[str] = None
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


# Convenience functions using cached execution
def fibonacci_cached(n: int) -> int:
    """Calculate Fibonacci via cached Mojo binary."""
    code = f"""
fn fibonacci(n: Int) -> Int:
    if n <= 1:
        return n
    var prev: Int = 0
    var curr: Int = 1
    for _ in range(2, n + 1):
        var next_val = prev + curr
        prev = curr
        curr = next_val
    return curr

fn main():
    print(fibonacci({n}))
"""
    result = mo_run_mojo_cached(code, use_cache=True)
    return int(result) if result else 0


def sum_squares_cached(n: int) -> int:
    """Calculate sum of squares via cached Mojo binary."""
    code = f"""
fn sum_squares(n: Int) -> Int:
    var total: Int = 0
    for i in range(1, n + 1):
        total += i * i
    return total

fn main():
    print(sum_squares({n}))
"""
    result = mo_run_mojo_cached(code, use_cache=True)
    return int(result) if result else 0


def is_prime_cached(n: int) -> bool:
    """Check if number is prime via cached Mojo binary."""
    code = f"""
fn is_prime(n: Int) -> Bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    var i: Int = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

fn main():
    print(is_prime({n}))
"""
    result = mo_run_mojo_cached(code, use_cache=True)
    return result == "True" if result else False


if __name__ == "__main__":
    print(f"Mojo version: {get_mojo_version()}\n")
    
    # First call - will compile and cache
    print("=== First calls (will compile) ===")
    print(f"Fibonacci(10): {fibonacci_cached(10)}")
    print(f"Sum squares 1-10: {sum_squares_cached(10)}")
    print(f"Is 17 prime? {is_prime_cached(17)}")
    
    print("\n=== Second calls (using cache) ===")
    print(f"Fibonacci(15): {fibonacci_cached(15)}")
    print(f"Sum squares 1-20: {sum_squares_cached(20)}")
    print(f"Is 23 prime? {is_prime_cached(23)}")
    
    print()
    cache_stats()
