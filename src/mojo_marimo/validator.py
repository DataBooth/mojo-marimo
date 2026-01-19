"""Simple validation for Mojo code before compilation."""

import re


def validate_mojo_code(code: str) -> tuple[bool, str | None]:
    """Perform basic validation on Mojo code.
    
    Args:
        code: Mojo source code to validate
        
    Returns:
        (is_valid, error_message) tuple
    """
    lines = code.strip().split('\n')
    
    # Check 1: Code is not empty
    if not code.strip():
        return False, "Empty code provided"
    
    # Check 2: Has a main function (required for executable)
    has_main = re.search(r'^fn main\(\)', code, re.MULTILINE)
    has_def_main = re.search(r'^def main\(\)', code, re.MULTILINE)
    
    if not (has_main or has_def_main):
        return False, "Missing 'fn main()' or 'def main()' - Mojo executables require a main function"
    
    # Check 3: Detect common indentation errors
    has_tabs = any('\t' in line for line in lines if line.strip())
    has_spaces = any(line.startswith(' ') and not line.startswith('\t') for line in lines)
    
    if has_tabs and has_spaces:
        return False, "Mixed tabs and spaces in indentation"
    
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        
        # Check for obvious indentation errors (statements at wrong level)
        stripped = line.lstrip()
        if stripped.startswith(('return ', 'var ', 'if ', 'for ', 'while ')):
            # These should be indented (inside a function/block)
            indent = len(line) - len(stripped)
            if indent == 0:
                return False, f"Line {i}: '{stripped.split()[0]}' at file scope (should be indented inside a function)"
    
    # Check 4: Basic syntax patterns
    # Look for common typos
    if re.search(r'fn\s+\w+\([^)]*\)\s*$', code, re.MULTILINE):
        # Function declaration without colon
        return False, "Function declaration missing colon (':') after parameters"
    
    # Check 5: Validate function/def syntax
    func_pattern = r'^(fn|def)\s+\w+\([^)]*\):'
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith(('fn ', 'def ')):
            if not ':' in stripped:
                return False, f"Line {i}: Function declaration missing colon (':') at end"
    
    return True, None


def get_validation_hint(error_msg: str) -> str:
    """Provide helpful hints for common validation errors."""
    hints = {
        "missing 'fn main()'": """
💡 Mojo executables require a main function:

fn main():
    # Your code here
    print("Hello")
""",
        "at file scope": """
💡 Statements like 'var', 'return', 'if', etc. must be inside a function:

fn main():
    var x = 42  # ✓ Correct
    print(x)

# var x = 42  # ✗ Wrong - can't be at file scope
""",
        "Mixed tabs and spaces": """
💡 Use consistent indentation (spaces recommended):

fn main():
    var x = 1    # ✓ All spaces
    print(x)     # ✓ All spaces
""",
        "missing colon": """
💡 Mojo function declarations need a colon:

fn compute(n: Int) -> Int:  # ✓ Colon at end
    return n * 2

fn compute(n: Int) -> Int   # ✗ Missing colon
""",
    }
    
    for key, hint in hints.items():
        if key.lower() in error_msg.lower():
            return hint
    
    return ""
