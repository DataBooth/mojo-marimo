"""mojo-marimo: Interactive Mojo integration for Python notebooks.

This package provides three approaches for running high-performance Mojo code
from Python/marimo notebooks:

1. Uncached Subprocess - Simple, transparent, best for development
2. Cached Binary - Fast repeated execution with SHA256-based caching
3. Decorator - Clean Pythonic syntax with cached performance

Example:
    from mojo_marimo import mojo

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

    result = fibonacci(10)
"""

__version__ = "0.1.0"
__author__ = "Michael Booth"
__email__ = "michael@databooth.com.au"

from mojo_marimo.mojo_decorator import mojo
from mojo_marimo.mo_run_cached import (
    clear_cache,
    cache_stats,
    fibonacci_cached,
    sum_squares_cached,
    is_prime_cached,
)
from mojo_marimo.compute_wrapper import (
    fibonacci,
    sum_squares,
    is_prime,
)

__all__ = [
    "mojo",
    "clear_cache",
    "cache_stats",
    "fibonacci_cached",
    "sum_squares_cached",
    "is_prime_cached",
    "fibonacci",
    "sum_squares",
    "is_prime",
]
