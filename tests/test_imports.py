"""Test basic imports and package structure."""

import pytest


def test_package_imports():
    """Test that the package can be imported."""
    import mojo_marimo
    
    assert mojo_marimo.__version__ == "0.1.0"
    assert mojo_marimo.__author__ == "Michael Booth"


def test_decorator_import():
    """Test that the decorator can be imported."""
    from mojo_marimo import mojo
    
    assert callable(mojo)


def test_core_functions_import():
    """Test that core functions can be imported."""
    from mojo_marimo import (
        run_mojo,
        clear_cache,
        cache_stats,
        get_mojo_version,
    )
    
    assert callable(run_mojo)
    assert callable(clear_cache)
    assert callable(cache_stats)
    assert callable(get_mojo_version)


def test_example_functions_import():
    """Test that example functions can be imported."""
    from mojo_marimo import fibonacci, sum_squares, is_prime
    
    assert callable(fibonacci)
    assert callable(sum_squares)
    assert callable(is_prime)


def test_all_exports():
    """Test that __all__ is properly defined."""
    import mojo_marimo
    
    expected = [
        # Core
        "run_mojo",
        "clear_cache",
        "cache_stats",
        "get_mojo_version",
        "mojo",
        # Examples
        "fibonacci",
        "sum_squares",
        "is_prime",
    ]
    
    assert set(mojo_marimo.__all__) == set(expected)
