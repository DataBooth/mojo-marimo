"""Mojo implementations for benchmarking against Python.

These implementations use the @mojo decorator for clean integration.
"""

from py_run_mojo import mojo


@mojo
def fibonacci(n: int) -> int:
    """
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
        print(fibonacci({{n}}))
    """
    ...


@mojo
def sum_squares(n: int) -> int:
    """
    fn sum_squares(n: Int) -> Int:
        var total: Int = 0
        for i in range(1, n + 1):
            total += i * i
        return total

    fn main():
        print(sum_squares({{n}}))
    """
    ...


@mojo
def is_prime(n: int) -> bool:
    """
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
        print(is_prime({{n}}))
    """
    ...


@mojo
def factorial(n: int) -> int:
    """
    fn factorial(n: Int) -> Int:
        if n <= 1:
            return 1
        var result: Int = 1
        for i in range(2, n + 1):
            result *= i
        return result

    fn main():
        print(factorial({{n}}))
    """
    ...


@mojo
def gcd(a: int, b: int) -> int:
    """
    fn gcd(a: Int, b: Int) -> Int:
        var x = a
        var y = b
        while y != 0:
            var temp = y
            y = x % y
            x = temp
        return x

    fn main():
        print(gcd({{a}}, {{b}}))
    """
    ...


@mojo
def count_primes(n: int) -> int:
    """
    fn is_prime(num: Int) -> Bool:
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False

        var i: Int = 3
        while i * i <= num:
            if num % i == 0:
                return False
            i += 2
        return True

    fn count_primes(n: Int) -> Int:
        var count: Int = 0
        for i in range(2, n + 1):
            if is_prime(i):
                count += 1
        return count

    fn main():
        print(count_primes({{n}}))
    """
    ...
