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
        
        # Skip imports, function/struct definitions, and comments
        if stripped.startswith(('from ', 'import ', 'fn ', 'def ', 'struct ', '#')):
            continue
            
        # Check for statements/expressions that should be inside functions
        if stripped.startswith(('return ', 'var ', 'if ', 'for ', 'while ', 'print(')):
            # These should be indented (inside a function/block)
            indent = len(line) - len(stripped)
            if indent == 0:
                keyword = stripped.split('(')[0] if '(' in stripped else stripped.split()[0]
                return False, f"Line {i}: '{keyword}' at file scope (must be inside a function)"
    
    # Check 4: Validate function/def syntax - missing colon
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith(('fn ', 'def ')):
            # Function declaration should end with :
            # Examples: fn foo():  or  fn bar(x: Int) -> Int:
            if not stripped.endswith(':'):
                # Make sure it's not a multi-line function (has opening brace on next line)
                # In Mojo, function declarations should have : on same line
                return False, f"Line {i}: Function declaration missing colon (':') at end"
    
    # Check 5: Common Python patterns that don't work in Mojo
    if re.search(r'\blet\s+\w+', code):
        return False, "'let' keyword is deprecated in Mojo - use 'var' instead"
    
    # Check 6: print statement without parentheses (Python 2 style)
    if re.search(r'^\s+print\s+(?!\()', code, re.MULTILINE):
        return False, "print requires parentheses: print(...) not print ..."
    
    # Check 7: Common typos in type annotations (case-sensitive)
    if re.search(r':\s*int\b', code):  # lowercase 'int' instead of 'Int'
        return False, "Use 'Int' (capitalized) for integer types in Mojo, not 'int'"
    
    if re.search(r':\s*str\b', code):  # lowercase 'str' instead of 'String'
        return False, "Use 'String' for string types in Mojo, not 'str'"
    
    if re.search(r':\s*bool\b', code):  # lowercase 'bool' instead of 'Bool'
        return False, "Use 'Bool' (capitalized) for boolean types in Mojo, not 'bool'"
    
    # Check 8: Missing parentheses in range/len
    if re.search(r'\brange\s+\d', code):  # range 10 instead of range(10)
        return False, "'range' requires parentheses: range(n) not range n"
    
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
        "'let' keyword is deprecated": """
💡 Mojo deprecated 'let' in favor of 'var':

fn main():
    var x = 42   # ✓ Use 'var'
    var y = 10   # ✓ Use 'var'
    # let z = 5  # ✗ 'let' is deprecated
""",
        "print requires parentheses": """
💡 Mojo requires parentheses for print (like Python 3):

fn main():
    print("Hello")      # ✓ Correct
    # print "Hello"    # ✗ Python 2 style doesn't work
""",
        "Use 'Int'": """
💡 Mojo type names are capitalized:

fn compute(n: Int) -> Int:   # ✓ Capitalized 'Int'
    return n * 2
    
# fn compute(n: int) -> int  # ✗ Python's 'int' doesn't work
""",
        "Use 'String'": """
💡 Mojo uses 'String' not 'str':

fn greet(name: String):      # ✓ Use 'String'
    print(name)
    
# fn greet(name: str)        # ✗ Python's 'str' doesn't work
""",
        "Use 'Bool'": """
💡 Mojo uses 'Bool' not 'bool':

fn is_valid(flag: Bool) -> Bool:  # ✓ Capitalized 'Bool'
    return flag
    
# fn is_valid(flag: bool)          # ✗ Python's 'bool' doesn't work
""",
        "'range' requires parentheses": """
💡 Function calls need parentheses:

fn main():
    for i in range(10):   # ✓ Correct
        print(i)
    # for i in range 10   # ✗ Missing parentheses
""",
    }
    
    for key, hint in hints.items():
        if key.lower() in error_msg.lower():
            return hint
    
    return ""
