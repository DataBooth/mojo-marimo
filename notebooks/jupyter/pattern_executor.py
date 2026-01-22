# %% [markdown]
# # run_mojo() Executor Pattern 🔥
# 
# Execute Mojo code dynamically from strings or files.
# 
# ## Key Concept
# 
# ```python
# from py_run_mojo import run_mojo
# 
# # Option 1: Inline code
# result = run_mojo("""
#     fn main():
#         print(42 * 42)
# """)
# 
# # Option 2: Execute file
# result = run_mojo("path/to/file.mojo")
# ```
# 
# Perfect for dynamic code generation, testing, or quick experiments.

# %%
from py_run_mojo import run_mojo, get_mojo_version

print(f"Mojo version: {get_mojo_version()}")

# %% [markdown]
# ## Example 1: Simple Computation

# %%
mojo_code = """
fn compute(n: Int) -> Int:
    return n * n

fn main():
    print(compute(42))
"""

result = run_mojo(mojo_code)
print(f"Result: {result}")

# %% [markdown]
# ## Example 2: Fibonacci from String

# %%
fib_code = """
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
    print(fibonacci(20))
"""

result = run_mojo(fib_code)
print(f"fibonacci(20) = {result}")

# %% [markdown]
# ## Example 3: Execute .mojo File

# %%
# Execute standalone Mojo file
result = run_mojo("../../examples/monte_carlo.mojo")
if result:
    print("Monte Carlo π estimation:")
    print(result)
else:
    print("Failed to execute")

# %% [markdown]
# ## Mojo Syntax Error Handling
# 
# The executor validates common Mojo syntax errors before compilation:

# %% [markdown]
# ### Error 1: Missing fn main()

# %%
bad_code_1 = """
fn compute(n: Int) -> Int:
    return n * n
"""

result = run_mojo(bad_code_1)
print(result)  # Will show validation error

# %% [markdown]
# ### Error 2: File-scope statements

# %%
bad_code_2 = """
print("Hello")  # Invalid - must be inside a function

fn main():
    print("World")
"""

result = run_mojo(bad_code_2)
print(result)

# %% [markdown]
# ### Error 3: Missing colon in function

# %%
bad_code_3 = """
fn compute(n: Int) -> Int  # Missing colon!
    return n * n

fn main():
    print(compute(5))
"""

result = run_mojo(bad_code_3)
print(result)

# %% [markdown]
# ### Error 4: Mixed indentation

# %%
bad_code_4 = """
fn main():
\tprint("tab")
    print("spaces")
"""

result = run_mojo(bad_code_4)
print(result)

# %% [markdown]
# ### Error 5: Deprecated let keyword

# %%
bad_code_5 = """
fn main():
    let x: Int = 42  # Deprecated! Use 'var' instead
    print(x)
"""

result = run_mojo(bad_code_5)
print(result)

# %% [markdown]
# ## All Validation Checks
# 
# The executor catches these common errors before compilation:
# 
# 1. **Missing `fn main()`** - Every Mojo program needs an entry point
# 2. **File-scope statements** - Code must be inside functions
# 3. **Missing colons** - Function definitions must end with `:`
# 4. **Mixed indentation** - Don't mix tabs and spaces
# 5. **Empty code** - Can't compile nothing!
# 6. **Deprecated `let`** - Use `var` instead
# 7. **Python-style print** - Use `print()` not `print "text"`
# 8. **Lowercase types** - Use `Int` not `int`, `String` not `str`, `Bool` not `bool`
# 9. **Missing parentheses** - Functions and range() need `()`
# 
# These validations provide quick feedback without waiting for compilation.

# %% [markdown]
# ## Performance Characteristics
# 
# - **First call**: ~1-2 seconds (compiles Mojo code)
# - **Subsequent calls with same code**: ~10-50ms (uses cached binary)
# - **Cache location**: `~/.mojo_cache/binaries/`
# 
# The executor pattern is perfect for dynamic code generation and testing.
