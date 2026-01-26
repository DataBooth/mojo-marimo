"""Test validator catches common Mojo errors."""

from py_run_mojo.validator import get_validation_hint, validate_mojo_code


def test_empty_code():
    """Validator catches empty code."""
    is_valid, error = validate_mojo_code("")
    assert not is_valid
    assert error and "empty" in error.lower()

    is_valid, error = validate_mojo_code("   \n  \n  ")
    assert not is_valid
    assert error and "empty" in error.lower()


def test_missing_main():
    """Validator catches missing main function."""
    code = """
    fn helper():
        print("I'm not main!")
    """
    is_valid, error = validate_mojo_code(code)
    assert not is_valid
    assert error and "main" in error.lower()


def test_mixed_indentation():
    """Validator catches mixed tabs and spaces."""
    code = "fn main():\n\tprint('tab')\n    print('spaces')"
    is_valid, error = validate_mojo_code(code)
    assert not is_valid
    assert error and ("indentation" in error.lower() or "mixed" in error.lower())


def test_file_scope_statement():
    """Validator catches statements at file scope."""
    code = """
fn main():
    print("ok")

var x = 10
"""
    is_valid, error = validate_mojo_code(code)
    assert not is_valid
    assert error and "file scope" in error.lower()


def test_missing_colon():
    """Validator catches missing colon in function definition."""
    code = """
fn main()
    print("oops")
"""
    is_valid, error = validate_mojo_code(code)
    assert not is_valid
    assert error and "colon" in error.lower()


def test_missing_colon_with_return_type():
    """Validator catches missing colon with return type annotation."""
    code = """
fn compute(n: Int) -> Int
    return n * 2

fn main():
    print(compute(5))
"""
    is_valid, error = validate_mojo_code(code)
    assert not is_valid
    assert error and "colon" in error.lower()


def test_valid_code():
    """Validator passes valid code."""
    code = """
fn main():
    print("Hello, Mojo!")
"""
    is_valid, error = validate_mojo_code(code)
    assert is_valid
    assert error is None


def test_validation_hints():
    """Test that hints are provided for errors."""
    # Missing main hint - use actual error message from validator
    hint = get_validation_hint(
        "Missing 'fn main()' or 'def main()' - Mojo executables require a main function"
    )
    assert "fn main()" in hint or "def main()" in hint

    # Mixed indentation hint
    hint = get_validation_hint("Mixed tabs and spaces in indentation")
    assert "consistent" in hint.lower()

    # File scope hint
    hint = get_validation_hint("Line 5: 'var' at file scope (should be indented inside a function)")
    assert "file scope" in hint.lower() or "inside a function" in hint.lower()

    # Missing colon hint
    hint = get_validation_hint("Function declaration missing colon (':') after parameters")
    assert "colon" in hint.lower() or ":" in hint

    # Unknown error returns empty string
    hint = get_validation_hint("some weird error")
    assert hint == ""


def test_multiple_errors():
    """Validator catches first error found."""
    code = """
var x = 10

fn helper()
    print("no colon and no main")
"""
    is_valid, error = validate_mojo_code(code)
    assert not is_valid
    assert error is not None  # Should catch at least one issue
