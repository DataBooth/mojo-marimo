"""Marimo notebook demonstrating the run_mojo() executor pattern.

Run with: marimo edit executor_notebook.py
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
    # run_mojo() Executor Pattern 🔥
    
    Direct execution of Mojo code from **text strings** or **.mojo files**.
    
    ## Two Ways to Use
    
    1. **run_mojo(mojo_code_string)** - Inline Mojo as Python string
    2. **run_mojo("/path/to/file.mojo")** - Execute external .mojo file
    """)
    return


@app.cell
def _():
    from mojo_marimo import run_mojo, get_mojo_version, clear_cache, cache_stats
    from pathlib import Path
    return Path, cache_stats, clear_cache, get_mojo_version, run_mojo


@app.cell
def _(get_mojo_version, mo):
    mo.md(f"**Mojo Version:** `{get_mojo_version()}`")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Pattern 1: Inline Mojo Code (String)
    
    Write Mojo code as a Python string and execute it directly:
    """)
    return


@app.cell
def _(mo):
    # Define Mojo code as a string template
    fibonacci_mojo = """
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
    print(fibonacci({n}))
"""
    
    # Display the code
    mo.md(f"""
    **Mojo Code:**
    ```mojo
    {fibonacci_mojo.strip()}
    ```
    """)
    return (fibonacci_mojo,)


@app.cell
def _(mo):
    fib_slider = mo.ui.slider(1, 40, value=10, label="n:", show_value=True)
    return (fib_slider,)


@app.cell
def _(fib_slider, fibonacci_mojo, mo, run_mojo):
    # Substitute parameter and run
    fib_code = fibonacci_mojo.format(n=fib_slider.value)
    fib_result = int(run_mojo(fib_code))
    
    mo.md(f"""
    {fib_slider}
    
    **Fibonacci({fib_slider.value})** = `{fib_result:,}`
    
    <details>
    <summary>Generated Mojo code (click to expand)</summary>
    
    ```mojo
    {fib_code.strip()}
    ```
    </details>
    """)
    return fib_code, fib_result


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Pattern 2: External .mojo File
    
    Execute a complete .mojo file directly:
    """)
    return


@app.cell
def _(Path):
    # Path to external .mojo file
    mojo_file = Path(__file__).parent.parent / "examples" / "examples.mojo"
    mojo_file_content = mojo_file.read_text()
    return mojo_file, mojo_file_content


@app.cell
def _(mo, mojo_file, mojo_file_content):
    mo.md(f"""
    **File:** `{mojo_file.name}`
    
    ```mojo
    {mojo_file_content}
    ```
    """)
    return


@app.cell
def _(mo):
    run_file_button = mo.ui.button(label="▶️ Run examples.mojo")
    return (run_file_button,)


@app.cell
def _(mo, mojo_file, run_file_button, run_mojo):
    # Run the .mojo file when button clicked
    file_result = None
    if run_file_button.value:
        file_result = run_mojo(str(mojo_file))
    
    if file_result:
        mo.md(f"""
        {run_file_button}
        
        **Output:**
        ```
        {file_result}
        ```
        
        ✅ Successfully executed `{mojo_file.name}`
        """)
    else:
        mo.md(f"{run_file_button}\n\n*Click button to run the .mojo file*")
    return (file_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Dynamic Code Generation Example
    
    The executor pattern is powerful for generating Mojo code programmatically:
    """)
    return


@app.cell
def _(mo):
    # UI for operation selection
    operation = mo.ui.dropdown(
        options=["add", "multiply", "power"],
        value="add",
        label="Operation:"
    )
    
    a_input = mo.ui.number(1, 100, value=5, label="a:")
    b_input = mo.ui.number(1, 100, value=3, label="b:")
    
    mo.md(f"{operation} {a_input} {b_input}")
    return a_input, b_input, operation


@app.cell
def _(a_input, b_input, mo, operation, run_mojo):
    # Generate Mojo code based on operation
    op_code_map = {
        "add": "a + b",
        "multiply": "a * b",
        "power": "a ** b"
    }
    
    dynamic_mojo = f"""
fn compute(a: Int, b: Int) -> Int:
    return {op_code_map[operation.value]}

fn main():
    print(compute({a_input.value}, {b_input.value}))
"""
    
    # Run the generated code
    dynamic_result = int(run_mojo(dynamic_mojo))
    
    mo.md(f"""
    **Generated Mojo:**
    ```mojo
    {dynamic_mojo.strip()}
    ```
    
    **Result:** `{a_input.value} {operation.value} {b_input.value} = {dynamic_result}`
    """)
    return dynamic_mojo, dynamic_result, op_code_map


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cache Management
    
    The executor uses SHA256-based caching to avoid recompilation:
    """)
    return


@app.cell
def _(cache_stats, mo):
    stats_button = mo.ui.button(label="📊 Show Cache Stats")
    return (stats_button,)


@app.cell
def _(cache_stats, mo, stats_button):
    if stats_button.value:
        # Capture cache stats output
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        cache_stats()
        sys.stdout = old_stdout
        
        stats_output = buffer.getvalue()
        
        mo.md(f"""
        {stats_button}
        
        ```
        {stats_output}
        ```
        """)
    else:
        mo.md(f"{stats_button}\n\n*Click to view cache statistics*")
    return buffer, old_stdout, stats_output


@app.cell
def _(clear_cache, mo):
    clear_button = mo.ui.button(label="🗑️ Clear Cache")
    return (clear_button,)


@app.cell
def _(clear_button, clear_cache, mo):
    if clear_button.value:
        clear_cache()
        mo.md(f"""
        {clear_button}
        
        ✅ Cache cleared! Next Mojo execution will recompile.
        """)
    else:
        mo.md(f"{clear_button}\n\n*Clear all cached Mojo binaries*")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Key Benefits
    
    ✅ **Flexible** - Use strings or files  
    ✅ **Dynamic** - Generate Mojo code programmatically  
    ✅ **Cached** - SHA256-based binary caching (~/.mojo_cache/binaries/)  
    ✅ **Fast** - First call ~1-2s, subsequent ~10-50ms  
    ✅ **Transparent** - See exactly what Mojo code runs  
    
    ## Pattern Templates
    
    ### String Pattern
    ```python
    from mojo_marimo import run_mojo
    
    mojo_code = '''
    fn compute(n: Int) -> Int:
        return n * n
    
    fn main():
        print(compute(10))
    '''
    
    result = run_mojo(mojo_code)
    ```
    
    ### File Pattern
    ```python
    from mojo_marimo import run_mojo
    
    result = run_mojo("/path/to/my_module.mojo")
    ```
    
    ## When to Use
    
    - ✅ Need to generate Mojo code dynamically
    - ✅ Working with larger Mojo modules (.mojo files)
    - ✅ Want explicit control over code generation
    - ✅ Sharing Mojo code across notebooks
    
    For cleaner inline functions, see `decorator_notebook.py`
    """)
    return


if __name__ == "__main__":
    app.run()
