"""Pure Python implementations for benchmarking against Mojo.

These are intentionally simple implementations to provide a fair baseline
comparison with Mojo. No numpy or other optimised libraries are used.
"""


def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number using iterative approach."""
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


def sum_squares(n: int) -> int:
    """Calculate sum of squares from 1 to n."""
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total


def is_prime(n: int) -> bool:
    """Check if number is prime using trial division."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a


def matrix_multiply_2x2(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    """Multiply two 2x2 matrices."""
    return [
        [
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ],
        [
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ],
    ]


def count_primes(n: int) -> int:
    """Count number of primes up to n."""
    count = 0
    for i in range(2, n + 1):
        if is_prime(i):
            count += 1
    return count
