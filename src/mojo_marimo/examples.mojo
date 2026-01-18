"""Simple Mojo functions for marimo integration example.

This module provides fast computation functions that can be called from Python/marimo.
"""

fn fibonacci(n: Int) -> Int:
    """Calculate the nth Fibonacci number iteratively."""
    if n <= 1:
        return n
    
    var prev: Int = 0
    var curr: Int = 1
    
    for _ in range(2, n + 1):
        var next_val = prev + curr
        prev = curr
        curr = next_val
    
    return curr


fn sum_squares(n: Int) -> Int:
    """Calculate the sum of squares from 1 to n."""
    var total: Int = 0
    for i in range(1, n + 1):
        total += i * i
    return total


fn is_prime(n: Int) -> Bool:
    """Check if a number is prime."""
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
    """Test the functions."""
    print("Fibonacci(10):", fibonacci(10))
    print("Sum of squares 1-10:", sum_squares(10))
    print("Is 17 prime?", is_prime(17))
    print("Is 18 prime?", is_prime(18))
