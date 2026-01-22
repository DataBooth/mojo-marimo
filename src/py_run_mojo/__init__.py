"""py-run-mojo: Run high-performance Mojo code from Python.

This package provides three approaches for running high-performance Mojo code
from any Python environment (notebooks, scripts, REPLs):

1. Uncached Subprocess - Simple, transparent, best for development
2. Cached Binary - Fast repeated execution with SHA256-based caching
3. Decorator - Clean Pythonic syntax with cached performance

Example:
    from py_run_mojo import mojo

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
            print(fibonacci({n}))
        '''
        pass

    result = fibonacci(10)
"""

__version__ = "0.1.2"
__author__ = "Michael Booth"
__email__ = "michael@databooth.com.au"

# Core functionality
from py_run_mojo.decorator import mojo
from py_run_mojo.executor import cache_stats, clear_cache, get_mojo_version, run_mojo
from py_run_mojo.validator import get_validation_hint, validate_mojo_code

__all__ = [
    "run_mojo",
    "clear_cache",
    "cache_stats",
    "get_mojo_version",
    "mojo",
    "validate_mojo_code",
    "get_validation_hint",
]
