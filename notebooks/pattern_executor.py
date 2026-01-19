"""run_mojo() Executor Pattern - Direct Mojo execution from strings or files.

Run: marimo edit pattern_executor.py
"""

import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # `run_mojo()` Executor Pattern 🔥

    Execute Mojo code from **strings** or **.mojo files**.

    ## Key Concept

    ```python
    from mojo_marimo import run_mojo

    # Pattern 1: Inline string
    mojo_code = '''
    fn main():
        print(42)
    '''
    result = run_mojo(mojo_code)

    # Pattern 2: .mojo file
    result = run_mojo("path/to/file.mojo")
    ```
    """)
    return


@app.cell
def _():
    from mojo_marimo import run_mojo, get_mojo_version
    from pathlib import Path
    return Path, get_mojo_version, run_mojo


@app.cell
def _(get_mojo_version, mo):
    mo.md(f"""
    **Mojo version:** `{get_mojo_version()}`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Pattern 1: Inline Mojo Code
    """)
    return


@app.cell
def _(mo, run_mojo):
    # Simple Mojo code as string
    simple_code = """
    fn main():
        print("Hello from Mojo!")
    """

    result1 = run_mojo(simple_code)

    mo.md(f"""
    **Mojo code:**
    ```mojo
    {simple_code.strip()}
    ```

    **Output:**  
    `{result1}`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Pattern 2: Fibonacci with Parameter
    """)
    return


@app.cell
def _(mo, run_mojo):
    # Mojo code with hardcoded value
    fib_code_10 = """
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
        print(fibonacci(10))
    """

    fib_result = run_mojo(fib_code_10)

    mo.md(f"""
    **Mojo code:**
    ```mojo
    {fib_code_10.strip()}
    ```

    **Output:**  
    `fibonacci(10) = {fib_result}`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Validation & Error Handling

    The executor validates Mojo code **before** compilation to catch common errors early.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Example 1: Missing `fn main()`
    """)
    return


@app.cell
def _(mo, run_mojo):
    no_main_code = """
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
    """

    result_no_main = run_mojo(no_main_code)

    mo.md(f"""
    **Mojo code:**
    ```mojo
    {no_main_code.strip()}
    ```

    **Result:** `{result_no_main}` ❌

    → Validation catches that executables need a `fn main()` function.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Example 2: Statements at File Scope
    """)
    return


@app.cell
def _(mo, run_mojo):
    file_scope_code = """
    var x = 42  # Error: can't declare variables at file scope

    fn main():
        print(x)
    """

    result_file_scope = run_mojo(file_scope_code)

    mo.md(f"""
    **Mojo code:**
    ```mojo
    {file_scope_code.strip()}
    ```

    **Result:** `{result_file_scope}` ❌

    → `var` must be inside a function, not at file scope.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Example 3: Missing Colon After Function
    """)
    return


@app.cell
def _(mo, run_mojo):
    no_colon_code = """
    fn compute(n: Int) -> Int
        return n * 2

    fn main():
        print(compute(5))
    """

    result_no_colon = run_mojo(no_colon_code)

    mo.md(f"""
    **Mojo code:**
    ```mojo
    {no_colon_code.strip()}
    ```

    **Result:** `{result_no_colon}` ❌

    → Function declarations need a colon (`:`) after the parameters.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Example 4: Mixed Tabs and Spaces
    """)
    return


@app.cell
def _(mo, run_mojo):
    # Note: using explicit \t in string to demonstrate
    mixed_indent_code = """fn main():
    \tvar x = 1  # Tab here
    print(x)   # Spaces here
    """

    result_mixed = run_mojo(mixed_indent_code)

    mo.md(f"""
    **Mojo code:**
    ```mojo
    {mixed_indent_code}
    ```

    **Result:** `{result_mixed}` ❌

    → Use consistent indentation (spaces recommended).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Example 5: Empty Code
    """)
    return


@app.cell
def _(mo, run_mojo):
    empty_code = """   

    """

    result_empty = run_mojo(empty_code)

    mo.md(f"""
    **Mojo code:**
    ```mojo
    {empty_code}
    ```

    **Result:** `{result_empty}` ❌

    → Empty or whitespace-only code is rejected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    **Validation Benefits:**
    - ✅ **Fast feedback** - Errors caught before compilation
    - ✅ **Helpful hints** - Specific error messages with examples
    - ✅ **Save time** - No waiting for compiler errors on obvious mistakes

    **Additional checks** (not shown above):
    - Deprecated `let` keyword (use `var` instead)
    - Python 2 style `print` without parentheses
    - Lowercase type names (`int` → `Int`, `str` → `String`, `bool` → `Bool`)
    - Missing parentheses in function calls (`range 10` → `range(10)`)

    **Note:** Both the decorator and executor patterns use the same validation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Pattern 3: Dynamic Code Generation
    """)
    return


@app.cell
def _(mo, run_mojo):
    # Generate Mojo code dynamically
    def compute_with_mojo(a, b, operation):
        """Generate and execute Mojo code for different operations."""
        operations = {
            "add": "a + b",
            "multiply": "a * b",
            "power": "a ** b"
        }

        mojo_code = f"""
        fn compute(a: Int, b: Int) -> Int:
            return {operations[operation]}

        fn main():
            print(compute({a}, {b}))
        """
        return run_mojo(mojo_code), mojo_code

    # Try different operations
    add_result, add_code = compute_with_mojo(5, 3, "add")
    mult_result, mult_code = compute_with_mojo(5, 3, "multiply")
    power_result, power_code = compute_with_mojo(5, 3, "power")

    mo.md(f"""
    **Dynamic code generation:**

    ```python
    5 + 3 = {add_result}
    5 * 3 = {mult_result}
    5 ** 3 = {power_result}
    ```

    <details>
    <summary>Generated Mojo code for power (click to expand)</summary>

    ```mojo
    {power_code.strip()}
    ```
    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Pattern 4: Execute .mojo File
    """)
    return


@app.cell
def _(Path, mo):
    # Load external .mojo file
    mojo_file = Path(__file__).parent.parent / "examples" / "examples.mojo"
    mojo_content = mojo_file.read_text()

    mo.md(f"""
    **File:** `{mojo_file.name}`

    ```mojo
    {mojo_content}
    ```
    """)
    return (mojo_file,)


@app.cell
def _(mo, mojo_file, run_mojo):
    # Execute the .mojo file
    file_result = run_mojo(str(mojo_file))

    mo.md(f"""
    **Executing** `{mojo_file.name}`:

    ```
    {file_result}
    ```

    ✅ Successfully executed external .mojo file
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    **Benefits:**
    - ✅ Flexible - strings or files
    - ✅ Dynamic - generate code programmatically
    - ✅ Transparent - see exactly what runs
    - ✅ Cached - SHA256-based binary caching

    **When to use:**
    - Dynamic code generation
    - External .mojo modules
    - Sharing code across notebooks
    - Need explicit control

    **See also:** `pattern_decorator.py` for cleaner inline functions
    """)
    return


if __name__ == "__main__":
    app.run()
