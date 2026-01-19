"""Mojo Extension Module Pattern (.so compilation).

This notebook demonstrates the alternative approach to running Mojo from Python:
compiling Mojo code to Python extension modules (.so files) for zero subprocess overhead.

Compare with:
- pattern_decorator.py (subprocess with caching)
- pattern_executor.py (direct run_mojo calls)
"""

import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    import time
    from pathlib import Path

    import marimo as mo

    # Add examples directory to path for Mojo imports
    examples_dir = Path(__file__).parent.parent / "examples"
    sys.path.insert(0, str(examples_dir))
    return examples_dir, mo, time


@app.cell
def _(mo):
    mo.md("""
    # Mojo Extension Module Pattern

    This notebook demonstrates using Mojo code compiled to Python extension modules (`.so` files).

    ## How It Works

    1. Write Mojo code with `PythonModuleBuilder` bindings
    2. Compile to `.so` using `mojo build --emit shared-lib`
    3. Import directly in Python (with `mojo.importer` for auto-compilation)
    4. Call functions with **zero subprocess overhead**

    ## Comparison with Other Patterns

    | Pattern | Overhead | Complexity | Use Case |
    |---------|----------|------------|----------|
    | **Extension (.so)** | ~0.01ms | High | Production, tight loops |
    | **Decorator** | ~10-50ms | Low | Development, notebooks |
    | **Executor** | ~10-50ms | Medium | Dynamic code generation |
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Import Extension Module

    ### Build Timing

    The build happens **automatically on first import**:

    1. **First import** (~1-2 seconds):
       - `mojo.importer` detects `.mojo` file
       - Runs `mojo build --emit shared-lib`
       - Saves `.so` to `__mojocache__/`
       - Imports the compiled module

    2. **Subsequent imports** (~instant):
       - `mojo.importer` finds cached `.so`
       - Checks if `.mojo` file changed (hash comparison)
       - Uses cached `.so` if unchanged
       - Recompiles only if source changed

    This is similar to Python's `.pyc` bytecode caching!
    """)
    return


@app.cell
def _():
    # Enable Mojo import hook for auto-compilation
    # Note: We don't return 'mojo' here to avoid namespace collision
    # with the @mojo decorator imported later from mojo_marimo
    import mojo.importer

    # Import our Mojo extension module
    # BUILD HAPPENS HERE: First import compiles .mojo → .so (~1-2s)
    # Subsequent imports use cached .so from __mojocache__/ (~instant)
    # Recompiles only when .mojo file changes
    import fibonacci_mojo_ext
    return (fibonacci_mojo_ext,)


@app.cell
def _(examples_dir, fibonacci_mojo_ext, mo):
    import os

    # Check if __mojocache__ exists to show build status
    cache_dir = examples_dir / "__mojocache__"
    cache_exists = cache_dir.exists()

    status_msg = (
        "📦 Using cached `.so` from `__mojocache__/` (build already done)"
        if cache_exists
        else "🔨 Compiled `.mojo` → `.so` on first import (~1-2s)"
    )

    mo.md(
        f"""
        ✅ Successfully imported `fibonacci_mojo_ext`

        {status_msg}

        Available functions:
        - `fibonacci(n)` - {fibonacci_mojo_ext.fibonacci.__doc__}
        - `is_prime(n)` - {fibonacci_mojo_ext.is_prime.__doc__}
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Example 1: Fibonacci
    """)
    return


@app.cell
def _(mo):
    n_slider = mo.ui.slider(1, 40, value=10, label="n", show_value=True)
    mo.md(f"**Calculate Fibonacci number:** {n_slider}")
    return (n_slider,)


@app.cell
def _(fibonacci_mojo_ext, mo, n_slider, time):
    # Call Mojo function directly - no subprocess!
    start = time.perf_counter()
    fib_result = fibonacci_mojo_ext.fibonacci(n_slider.value)
    elapsed_ms = (time.perf_counter() - start) * 1000

    mo.md(
        f"""
        **fibonacci({n_slider.value})** = {fib_result:,}

        Execution time: {elapsed_ms:.3f}ms

        ⚡ **Direct function call** - no subprocess overhead!
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Example 2: Prime Number Testing
    """)
    return


@app.cell
def _(mo):
    prime_input = mo.ui.number(
        start=1, stop=10_000_000, value=104729, label="Test if prime", step=1
    )
    mo.md(f"**Enter a number:** {prime_input}")
    return (prime_input,)


@app.cell
def _(fibonacci_mojo_ext, mo, prime_input, time):
    start_prime = time.perf_counter()
    is_prime_result = fibonacci_mojo_ext.is_prime(prime_input.value)
    elapsed_prime_ms = (time.perf_counter() - start_prime) * 1000

    result_emoji = "✅" if is_prime_result else "❌"

    mo.md(
        f"""
        {result_emoji} **{prime_input.value:,}** is {"" if is_prime_result else "not "}prime

        Execution time: {elapsed_prime_ms:.3f}ms
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Performance Comparison
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    Let's compare the extension module approach with the decorator pattern:
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Trade-offs
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Extension Module (.so) Advantages

    ✅ **Zero subprocess overhead** - direct Python calls
    ✅ **100-1000x faster** for simple operations or tight loops
    ✅ **Production ready** - standard Python extension module
    ✅ **Auto-compilation** - `mojo.importer` handles rebuilding

    ### Extension Module Disadvantages

    ❌ **More complex Mojo code** - requires `PyInit_*()` boilerplate
    ❌ **Different API** - functions must take `PythonObject` arguments
    ❌ **Learning curve** - need to understand `PythonModuleBuilder`
    ❌ **Less flexible** - harder to generate code dynamically

    ### When to Use Extension Modules

    - Production deployments
    - Functions called thousands of times
    - Performance-critical tight loops
    - When every millisecond counts
    - Stable APIs that don't change frequently

    ### When to Use Decorator Pattern

    - Interactive notebook development
    - Prototyping and exploration
    - Educational content
    - When simplicity > absolute performance
    - Compute-intensive tasks (>100ms) where subprocess overhead is negligible
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Technical Details
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Mojo Code Structure

    Extension modules require specific structure:

    ```mojo
    from python import PythonObject
    from python.bindings import PythonModuleBuilder

    @export
    fn PyInit_mymodule() -> PythonObject:
        var mb = PythonModuleBuilder("mymodule")
        mb.def_function[my_func]("my_func")
        return mb.finalize()

    fn my_func(py_arg: PythonObject) raises -> PythonObject:
        var arg = Int(py=py_arg)  # Convert from Python
        var result = arg * 2
        return PythonObject(result)  # Convert to Python
    ```

    ### Compilation

    **Manual:**
    ```bash
    mojo build mymodule.mojo --emit shared-lib -o mymodule.so
    ```

    **Auto (recommended):**
    ```python
    import mojo.importer  # Enables auto-compilation
    import mymodule  # Compiles .mojo → .so automatically
    ```

    ### Cache Location

    Compiled `.so` files are cached in `__mojocache__/`:
    ```
    project/
    ├── mymodule.mojo
    └── __mojocache__/
        └── mymodule.hash-ABC123.so
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## See Also
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    - [examples/fibonacci_mojo_ext.mojo](../examples/fibonacci_mojo_ext.mojo) - Source code
    - [examples/EXTENSION_MODULES.md](../examples/EXTENSION_MODULES.md) - Detailed guide
    - [Mojo docs: Calling Mojo from Python](https://docs.modular.com/mojo/manual/python/mojo-from-python/)
    - [docs/COMPILED_LANGUAGES.md](../docs/COMPILED_LANGUAGES.md) - Integration patterns
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
