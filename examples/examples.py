"""Example Mojo functions demonstrating the cached executor.

These are convenience wrappers that demonstrate how to use the executor
for common computational tasks.
"""

import sys
from pathlib import Path

# Add src to path when run as script
if __name__ == "__main__":
    src_path = Path(__file__).parent.parent / "src"
    sys.path.insert(0, str(src_path))

from mojo_marimo.executor import run_mojo


def fibonacci(n: int) -> int:
    """Calculate Fibonacci number via cached Mojo binary.
    
    Args:
        n: The Fibonacci number to calculate
        
    Returns:
        The nth Fibonacci number
    """
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
    result = run_mojo(code)
    return int(result) if result else 0


def sum_squares(n: int) -> int:
    """Calculate sum of squares 1² + 2² + ... + n² via cached Mojo binary.
    
    Args:
        n: Calculate sum up to this number
        
    Returns:
        The sum of squares from 1 to n
    """
    code = f"""
fn sum_squares(n: Int) -> Int:
    var total: Int = 0
    for i in range(1, n + 1):
        total += i * i
    return total

fn main():
    print(sum_squares({n}))
"""
    result = run_mojo(code)
    return int(result) if result else 0


def is_prime(n: int) -> bool:
    """Check if number is prime via cached Mojo binary.
    
    Args:
        n: The number to check
        
    Returns:
        True if n is prime, False otherwise
    """
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
    result = run_mojo(code)
    return result == "True" if result else False


if __name__ == "__main__":
    # Imports already available from above
    from mojo_marimo.executor import get_mojo_version, cache_stats
    
    print(f"Mojo version: {get_mojo_version()}\n")
    
    # First calls - will compile and cache
    print("=== First calls (will compile) ===")
    print(f"Fibonacci(10): {fibonacci(10)}")
    print(f"Sum squares 1-10: {sum_squares(10)}")
    print(f"Is 17 prime? {is_prime(17)}")
    
    print("\n=== Second calls (using cache) ===")
    print(f"Fibonacci(15): {fibonacci(15)}")
    print(f"Sum squares 1-20: {sum_squares(20)}")
    print(f"Is 23 prime? {is_prime(23)}")
    
    print()
    cache_stats()
