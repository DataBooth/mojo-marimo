"""Tests for the executor module."""

import tempfile
from pathlib import Path

import pytest


def test_run_mojo_with_simple_code():
    """Test basic code execution."""
    from py_run_mojo.executor import run_mojo

    code = """
def main():
    print("test output")
"""
    result = run_mojo(code)
    assert result == "test output"


def test_run_mojo_with_arithmetic():
    """Test code that performs computation."""
    from py_run_mojo.executor import run_mojo

    code = """
def main():
    var result = 42 + 8
    print(result)
"""
    result = run_mojo(code)
    assert result == "50"


def test_cache_enabled_by_default():
    """Test that caching is enabled by default."""
    from py_run_mojo.executor import clear_cache, run_mojo

    # Clear cache first
    clear_cache()

    code = """
def main():
    print("cached test")
"""

    # First call should cache
    result1 = run_mojo(code, use_cache=True)
    # Second call should use cache
    result2 = run_mojo(code, use_cache=True)

    assert result1 == result2 == "cached test"


def test_cache_disabled():
    """Test that caching can be disabled."""
    from py_run_mojo.executor import run_mojo

    code = """
def main():
    print("no cache")
"""

    # Both calls compile fresh
    result1 = run_mojo(code, use_cache=False)
    result2 = run_mojo(code, use_cache=False)

    assert result1 == result2 == "no cache"


def test_clear_cache():
    """Test cache clearing functionality."""
    from py_run_mojo.executor import clear_cache, run_mojo

    code = """
def main():
    print("test")
"""

    # Create cache entry
    run_mojo(code, use_cache=True)

    # Clear should not raise
    clear_cache()


def test_cache_stats():
    """Test cache statistics functionality."""
    from py_run_mojo.executor import cache_stats, clear_cache

    clear_cache()

    # Should not raise even with empty cache
    cache_stats()


def test_get_mojo_version():
    """Test Mojo version retrieval."""
    from py_run_mojo.executor import get_mojo_version

    version = get_mojo_version()
    # Should return something (or "Unknown" if mojo not found)
    assert isinstance(version, str)
    assert len(version) > 0


def test_run_mojo_with_file():
    """Test execution from a .mojo file."""
    from py_run_mojo.executor import run_mojo

    # Create temporary .mojo file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mojo", delete=False) as f:
        f.write('def main():\n    print("from file")')
        temp_path = f.name

    try:
        result = run_mojo(temp_path)
        assert result == "from file"
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_empty_source():
    """Test handling of empty source."""
    from py_run_mojo.executor import run_mojo

    result = run_mojo("")
    assert result is None


def test_invalid_mojo_code():
    """Test handling of invalid Mojo code."""
    from py_run_mojo.executor import run_mojo

    code = """
def main(:
    invalid syntax here
"""

    result = run_mojo(code)
    # Should return None on compilation error
    assert result is None


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, "1"),  # 0! = 1 by definition
        (1, "1"),
        (5, "120"),  # 5! = 120
    ],
)
def test_factorial_computation(n, expected):
    """Test parameterized factorial computation."""
    from py_run_mojo.executor import run_mojo

    code = f"""
def factorial(n: Int) -> Int:
    if n <= 1:
        return 1
    var result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def main():
    print(factorial({n}))
"""

    result = run_mojo(code)
    assert result == expected


def test_run_mojo_with_long_source_string():
    """Long multi-line source must be treated as code, not a file path.

    Regression test: on Python 3.13+, pathlib.is_file() re-raises
    ENAMETOOLONG instead of returning False for over-long "paths".
    """
    from py_run_mojo.executor import run_mojo

    code = """
def main():
    var total = 0
    for i in range(10):
        total += i
    # This comment exists only to push the source past 255 bytes so that
    # treating it as a file path would raise ENAMETOOLONG on Python 3.13+.
    # Regression test for pathlib.is_file() re-raising instead of returning
    # False when handed inline source code instead of a real path.
    print(total)
"""
    assert len(code.encode()) > 255  # exceed filesystem NAME_MAX
    assert run_mojo(code) == "45"


def test_run_mojo_with_long_single_line_source():
    """Long single-line source (no newlines) must not raise from the path check."""
    from py_run_mojo.executor import run_mojo

    payload = "x" * 300
    code = f'def main(): print("{payload}")'
    assert "\n" not in code and len(code.encode()) > 255
    assert run_mojo(code) == payload


def test_find_mojo_binary_prefers_path(monkeypatch):
    """mojo found on PATH is used when available."""
    from py_run_mojo import executor

    monkeypatch.setattr(executor.shutil, "which", lambda name: "/usr/bin/mojo")
    assert executor._find_mojo_binary() == "/usr/bin/mojo"


def test_find_mojo_binary_falls_back_to_interpreter_dir(monkeypatch):
    """Without mojo on PATH, use the binary next to the running interpreter
    (pip-installed mojo package in the same virtualenv)."""
    import sys
    from pathlib import Path

    from py_run_mojo import executor

    monkeypatch.setattr(executor.shutil, "which", lambda name: None)
    expected = Path(sys.executable).parent / "mojo"
    assert expected.is_file()  # sanity: venv must have mojo beside python
    assert executor._find_mojo_binary() == str(expected)


def test_find_mojo_binary_defaults_to_literal(monkeypatch, tmp_path):
    """With no mojo anywhere, fall back to bare 'mojo' so the subprocess
    raises the standard FileNotFoundError."""
    from py_run_mojo import executor

    monkeypatch.setattr(executor.shutil, "which", lambda name: None)
    monkeypatch.setattr(executor.sys, "executable", str(tmp_path / "python"))
    assert executor._find_mojo_binary() == "mojo"
