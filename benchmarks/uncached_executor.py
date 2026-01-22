"""Uncached Mojo executor functions for benchmarking.

These use run_mojo directly without caching to show the compilation overhead.
"""

from py_run_mojo import run_mojo


def fibonacci(n: int) -> int:
    """Fibonacci using uncached executor."""
    mojo_code = f"""
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
    result = run_mojo(mojo_code)
    return int(result) if result else 0


def sum_squares(n: int) -> int:
    """Sum of squares using uncached executor."""
    mojo_code = f"""
fn sum_squares(n: Int) -> Int:
    var total: Int = 0
    for i in range(1, n + 1):
        total += i * i
    return total

fn main():
    print(sum_squares({n}))
"""
    result = run_mojo(mojo_code)
    return int(result) if result else 0


def is_prime(n: int) -> bool:
    """Prime check using uncached executor."""
    mojo_code = f"""
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
    result = run_mojo(mojo_code)
    return result == "True" if result else False
