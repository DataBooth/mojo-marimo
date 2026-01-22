"""Test basic imports and package structure."""


def test_package_imports():
    """Test that the package can be imported."""
    import py_run_mojo

    assert py_run_mojo.__version__ == "0.1.2"
    assert py_run_mojo.__author__ == "Michael Booth"


def test_decorator_import():
    """Test that the decorator can be imported."""
    from py_run_mojo import mojo

    assert callable(mojo)


def test_core_functions_import():
    """Test that core functions can be imported."""
    from py_run_mojo import (
        cache_stats,
        clear_cache,
        get_mojo_version,
        run_mojo,
    )

    assert callable(run_mojo)
    assert callable(clear_cache)
    assert callable(cache_stats)
    assert callable(get_mojo_version)


def test_decorator_definition():
    """Test that decorator can define functions."""
    from py_run_mojo import mojo

    # Can define a decorated function
    @mojo
    def test_func(n: int) -> int:
        """fn main(): print(42)"""
        ...

    assert callable(test_func)


def test_all_exports():
    """Test that __all__ is properly defined."""
    import py_run_mojo

    expected = [
        "run_mojo",
        "clear_cache",
        "cache_stats",
        "get_mojo_version",
        "mojo",
        "validate_mojo_code",
        "get_validation_hint",
    ]

    assert set(py_run_mojo.__all__) == set(expected)
