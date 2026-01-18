"""Tests for the executor module."""

import pytest
from pathlib import Path
import tempfile


def test_run_mojo_with_simple_code():
    """Test basic code execution."""
    from mojo_marimo.executor import run_mojo
    
    code = """
fn main():
    print("test output")
"""
    result = run_mojo(code)
    assert result == "test output"


def test_run_mojo_with_arithmetic():
    """Test code that performs computation."""
    from mojo_marimo.executor import run_mojo
    
    code = """
fn main():
    var result = 42 + 8
    print(result)
"""
    result = run_mojo(code)
    assert result == "50"


def test_cache_enabled_by_default():
    """Test that caching is enabled by default."""
    from mojo_marimo.executor import run_mojo, clear_cache
    
    # Clear cache first
    clear_cache()
    
    code = """
fn main():
    print("cached test")
"""
    
    # First call should cache
    result1 = run_mojo(code, use_cache=True)
    # Second call should use cache
    result2 = run_mojo(code, use_cache=True)
    
    assert result1 == result2 == "cached test"


def test_cache_disabled():
    """Test that caching can be disabled."""
    from mojo_marimo.executor import run_mojo
    
    code = """
fn main():
    print("no cache")
"""
    
    # Both calls compile fresh
    result1 = run_mojo(code, use_cache=False)
    result2 = run_mojo(code, use_cache=False)
    
    assert result1 == result2 == "no cache"


def test_clear_cache():
    """Test cache clearing functionality."""
    from mojo_marimo.executor import run_mojo, clear_cache
    
    code = """
fn main():
    print("test")
"""
    
    # Create cache entry
    run_mojo(code, use_cache=True)
    
    # Clear should not raise
    clear_cache()


def test_cache_stats():
    """Test cache statistics functionality."""
    from mojo_marimo.executor import cache_stats, clear_cache
    
    clear_cache()
    
    # Should not raise even with empty cache
    cache_stats()


def test_get_mojo_version():
    """Test Mojo version retrieval."""
    from mojo_marimo.executor import get_mojo_version
    
    version = get_mojo_version()
    # Should return something (or "Unknown" if mojo not found)
    assert isinstance(version, str)
    assert len(version) > 0


def test_run_mojo_with_file():
    """Test execution from a .mojo file."""
    from mojo_marimo.executor import run_mojo
    
    # Create temporary .mojo file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mojo', delete=False) as f:
        f.write('fn main():\n    print("from file")')
        temp_path = f.name
    
    try:
        result = run_mojo(temp_path)
        assert result == "from file"
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_empty_source():
    """Test handling of empty source."""
    from mojo_marimo.executor import run_mojo
    
    result = run_mojo("")
    assert result is None


def test_invalid_mojo_code():
    """Test handling of invalid Mojo code."""
    from mojo_marimo.executor import run_mojo
    
    code = """
fn main(:
    invalid syntax here
"""
    
    result = run_mojo(code)
    # Should return None on compilation error
    assert result is None


@pytest.mark.parametrize("n,expected", [
    (0, "1"),  # 0! = 1 by definition
    (1, "1"),
    (5, "120"),  # 5! = 120
])
def test_factorial_computation(n, expected):
    """Test parameterized factorial computation."""
    from mojo_marimo.executor import run_mojo
    
    code = f"""
fn factorial(n: Int) -> Int:
    if n <= 1:
        return 1
    var result = 1
    for i in range(2, n + 1):
        result *= i
    return result

fn main():
    print(factorial({n}))
"""
    
    result = run_mojo(code)
    assert result == expected
