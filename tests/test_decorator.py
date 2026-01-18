"""Tests for the @mojo decorator."""

import pytest


def test_decorator_basic():
    """Test basic decorator functionality."""
    from mojo_marimo import mojo
    
    @mojo
    def simple_func(n: int) -> int:
        """
        fn main():
            print(42)
        """
        pass
    
    result = simple_func(10)
    assert result == 42


def test_decorator_with_parameter_substitution():
    """Test that parameters are properly substituted."""
    from mojo_marimo import mojo
    
    @mojo
    def echo(n: int) -> int:
        """
        fn main():
            print({{n}})
        """
        pass
    
    assert echo(5) == 5
    assert echo(100) == 100


def test_decorator_returns_int():
    """Test int return type conversion."""
    from mojo_marimo import mojo
    
    @mojo
    def double(n: int) -> int:
        """
        fn main():
            var result = {{n}} * 2
            print(result)
        """
        pass
    
    assert double(5) == 10
    assert double(21) == 42


def test_decorator_returns_bool():
    """Test bool return type conversion."""
    from mojo_marimo import mojo
    
    @mojo
    def is_positive(n: int) -> bool:
        """
        fn main():
            var result = {{n}} > 0
            print(result)
        """
        pass
    
    assert is_positive(5) is True
    assert is_positive(-5) is False
    assert is_positive(0) is False


def test_decorator_with_multiple_params():
    """Test decorator with multiple parameters."""
    from mojo_marimo import mojo
    
    @mojo
    def add(a: int, b: int) -> int:
        """
        fn main():
            var result = {{a}} + {{b}}
            print(result)
        """
        pass
    
    assert add(2, 3) == 5
    assert add(10, 20) == 30


def test_decorator_caching():
    """Test that decorator uses caching."""
    from mojo_marimo import mojo
    from mojo_marimo.executor import clear_cache
    
    clear_cache()
    
    @mojo
    def cached_func(n: int) -> int:
        """
        fn main():
            print({{n}})
        """
        pass
    
    # Multiple calls with same implementation should use cache
    result1 = cached_func(10)
    result2 = cached_func(20)  # Different param but same code structure
    
    assert result1 == 10
    assert result2 == 20


def test_decorator_without_docstring():
    """Test that decorator raises error without docstring."""
    from mojo_marimo import mojo
    
    with pytest.raises(ValueError, match="no docstring"):
        @mojo
        def no_doc(n: int) -> int:
            pass


def test_decorator_preserves_function_name():
    """Test that decorator preserves function metadata."""
    from mojo_marimo import mojo
    
    @mojo
    def my_function(n: int) -> int:
        """
        fn main():
            print(42)
        """
        pass
    
    assert my_function.__name__ == "my_function"


def test_decorator_with_complex_mojo_code():
    """Test decorator with more complex Mojo implementation."""
    from mojo_marimo import mojo
    
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
        pass
    
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55


@pytest.mark.parametrize("n,expected", [
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (18, False),
])
def test_decorator_prime_check(n, expected):
    """Test decorator with prime checking logic."""
    from mojo_marimo import mojo
    
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
        pass
    
    assert is_prime(n) == expected
