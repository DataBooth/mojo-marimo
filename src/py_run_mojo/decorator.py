"""Decorator for inline Mojo code execution.

This demonstrates the decorator pattern discussed in the Modular forum.
Currently uses cached binaries (same as mo_run_cached) but structured
as a decorator for cleaner syntax.

Future enhancement: compile to Python extension modules for zero subprocess overhead.
"""

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any

from py_run_mojo.executor import get_mojo_version, run_mojo


def mojo(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to execute Mojo code from function docstring.

    The function's docstring should contain valid Mojo code that
    implements the logic. The function signature determines the
    interface.

    Usage:
        @mojo
        def fibonacci(n: int) -> int:
            '''
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
            '''
            pass

        # Use like normal Python function
        result = fibonacci(10)

    Note: Use {{param_name}} in docstring as placeholder for parameter substitution.
    """

    # Extract Mojo code template from docstring
    mojo_template = func.__doc__
    if not mojo_template:
        raise ValueError(f"Function {func.__name__} has no docstring with Mojo code")

    # Get function signature for parameter handling
    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Bind arguments to parameter names
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        # Substitute parameters into Mojo template
        mojo_code = mojo_template
        for param_name, param_value in bound.arguments.items():
            placeholder = f"{{{{{param_name}}}}}"  # {{param}} in docstring
            mojo_code = mojo_code.replace(placeholder, str(param_value))

        # Execute via cached binary
        result = run_mojo(mojo_code, use_cache=True)

        # Convert result based on return type annotation
        return_type = sig.return_annotation
        if return_type is int:
            return int(result) if result else 0
        if return_type is bool:
            return result == "True" if result else False
        if return_type is float:
            return float(result) if result else 0.0
        return result

    return wrapper


# Example decorated functions


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


if __name__ == "__main__":
    print(f"Mojo version: {get_mojo_version()}\n")
    print("=== Using @mojo decorator ===\n")

    # Call decorated functions like normal Python
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"sum_squares(10) = {sum_squares(10)}")
    print(f"is_prime(17) = {is_prime(17)}")
    print(f"is_prime(18) = {is_prime(18)}")

    print("\n=== Cached calls (should be fast) ===\n")
    print(f"fibonacci(15) = {fibonacci(15)}")
    print(f"sum_squares(20) = {sum_squares(20)}")
    print(f"is_prime(97) = {is_prime(97)}")
