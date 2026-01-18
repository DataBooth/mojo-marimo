"""Helper to run Mojo code from marimo notebooks.

Based on mo_run_mojo pattern for executing Mojo code via subprocess.
"""

from functools import cache
from pathlib import Path
from typing import Optional
import subprocess
import tempfile


@cache
def get_mojo_version() -> str:
    """Get the installed Mojo version."""
    try:
        return subprocess.getoutput("mojo --version").strip()
    except Exception:
        return "Unknown"


def mo_run_mojo(
    source: str,
    echo_code: bool = False,
    echo_output: bool = False,
    extra_args: Optional[list[str]] = None,
) -> Optional[str]:
    """
    Run Mojo code from a file path or string.
    
    Args:
        source: File path or Mojo code string.
        echo_code: Print the code before running.
        echo_output: Print the output after running.
        extra_args: Optional list of extra arguments for 'mojo run'.
    
    Returns:
        The stdout output if successful, else None.
    """
    if not source.strip():
        print("Error: Empty source provided.")
        return None
    
    path = Path(source)
    filepath: str
    mojo_code: str
    
    if path.is_file():
        filepath = str(path)
        try:
            mojo_code = path.read_text()
        except OSError as e:
            print(f"Error reading file {path}: {e}")
            return None
        if echo_code:
            print(f"### Echoing Mojo code from file: {path}\n")
    else:
        # Treat as code string, write to temp file
        mojo_code = source
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mojo")
        filepath = tmp.name
        try:
            tmp.write(mojo_code.encode('utf-8'))
            tmp.close()
        except OSError as e:
            print(f"Error writing temp file: {e}")
            return None
        if echo_code:
            print("### Echoing Mojo code from string input\n")
    
    if echo_code:
        print(mojo_code)
        print("-" * 80)
    
    cmd = ['mojo', 'run', filepath]
    if extra_args:
        cmd.extend(extra_args)
    
    try:
        result = subprocess.run(
            cmd,
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
            print(f"\n### Mojo errors:\n{result.stderr}")
        if result.returncode != 0:
            return None
        return output
    except subprocess.SubprocessError as e:
        print(f"Subprocess error running Mojo: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        if not path.is_file():
            try:
                Path(filepath).unlink(missing_ok=True)
            except OSError:
                pass


def fibonacci(n: int) -> int:
    """Calculate Fibonacci via Mojo."""
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
    result = mo_run_mojo(code, echo_code=False, echo_output=False)
    return int(result) if result else 0


def sum_squares(n: int) -> int:
    """Calculate sum of squares via Mojo."""
    code = f"""
fn sum_squares(n: Int) -> Int:
    var total: Int = 0
    for i in range(1, n + 1):
        total += i * i
    return total

fn main():
    print(sum_squares({n}))
"""
    result = mo_run_mojo(code, echo_code=False, echo_output=False)
    return int(result) if result else 0


def is_prime(n: int) -> bool:
    """Check if number is prime via Mojo."""
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
    result = mo_run_mojo(code, echo_code=False, echo_output=False)
    return result == "True" if result else False


if __name__ == "__main__":
    print(f"Mojo version: {get_mojo_version()}")
    print(f"Fibonacci(10): {fibonacci(10)}")
    print(f"Sum of squares 1-10: {sum_squares(10)}")
    print(f"Is 17 prime? {is_prime(17)}")
    print(f"Is 18 prime? {is_prime(18)}")
