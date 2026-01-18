"""Pytest configuration for mojo-marimo tests."""

import pytest
import subprocess


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "requires_mojo: mark test as requiring mojo on PATH"
    )


def check_mojo_available():
    """Check if mojo command is available."""
    try:
        result = subprocess.run(
            ["mojo", "--version"],
            capture_output=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


@pytest.fixture(scope="session", autouse=True)
def check_mojo_env():
    """Check if mojo is available and skip tests if not."""
    if not check_mojo_available():
        pytest.skip(
            "Mojo not found on PATH. Install: curl https://get.modular.com | sh - && modular install mojo",
            allow_module_level=True
        )


@pytest.fixture
def mojo_code_simple():
    """Fixture providing simple Mojo code for testing."""
    return """
fn main():
    print("test")
"""


@pytest.fixture
def mojo_code_arithmetic():
    """Fixture providing Mojo code with arithmetic."""
    return """
fn main():
    var result = 10 + 5
    print(result)
"""
