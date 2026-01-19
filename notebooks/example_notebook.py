"""Marimo notebook demonstrating Mojo integration.

Run with: marimo edit example_notebook.py
Or as app: marimo run example_notebook.py
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
    # Mojo + Marimo Integration Demo 🔥

    This notebook demonstrates running **real Mojo code** within a reactive marimo notebook using `mo_run_mojo`.

    Each computation executes actual Mojo code via subprocess - no Python fallbacks!
    """)
    return


@app.cell
def _():
    # Add examples to path
    import sys
    from pathlib import Path

    examples_path = Path(__file__).parent.parent / "examples"
    sys.path.insert(0, str(examples_path))

    # Import our compute functions (runs real Mojo code!)
    from examples import fibonacci, is_prime, sum_squares
    from mojo_marimo import get_mojo_version

    return fibonacci, get_mojo_version, is_prime, sum_squares


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Fibonacci Calculator
    """)
    return


@app.cell
def _(mo):
    # Interactive slider for Fibonacci input
    fib_slider = mo.ui.slider(start=1, stop=30, value=10, label="n:", show_value=True)
    return (fib_slider,)


@app.cell
def _(fib_slider, fibonacci, mo):
    fib_result = fibonacci(fib_slider.value)

    mo.md(
        f"""
        **Fibonacci({fib_slider.value})** = `{fib_result:,}`

        {fib_slider}
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Sum of Squares
    """)
    return


@app.cell
def _(mo):
    # Input for sum of squares
    sum_sq_slider = mo.ui.slider(start=1, stop=100, value=10, label="n:", show_value=True)
    return (sum_sq_slider,)


@app.cell
def _(mo, sum_sq_slider, sum_squares):
    sum_result = sum_squares(sum_sq_slider.value)

    mo.md(
        f"""
        **Sum of squares 1 to {sum_sq_slider.value}** = `{sum_result:,}`

        Formula: 1² + 2² + 3² + ... + {sum_sq_slider.value}² = {sum_result:,}

        {sum_sq_slider}
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Prime Number Checker
    """)
    return


@app.cell
def _(mo):
    # Number input for prime checking
    prime_input = mo.ui.number(start=1, stop=10000, value=17, label="Check if prime:")
    return (prime_input,)


@app.cell
def _(is_prime, mo, prime_input):
    is_prime_result = is_prime(prime_input.value)

    status = "✓ Prime" if is_prime_result else "✗ Not Prime"
    color = "green" if is_prime_result else "red"

    mo.md(
        f"""
        {prime_input}

        **{prime_input.value}** is <span style="color: {color}; font-weight: bold;">{status}</span>
        """
    )
    return


@app.cell(hide_code=True)
def _(get_mojo_version, mo):
    mo.md(f"""
    ---

    ## About This Demo

    **Mojo Version:** `{get_mojo_version()}`

    This notebook uses **cached Mojo execution** via `run_mojo()`:

    1. Each function call generates Mojo source code
    2. Code is compiled to a binary on first call
    3. Binary is cached by SHA256 hash
    4. Subsequent calls reuse the cached binary (~10-50ms)
    5. Output is parsed and returned to marimo

    ### Performance

    ✅ **First call**: ~1-2s (compile + run)  
    ✅ **Subsequent calls**: ~10-50ms (run only)  
    ✅ **Cache persists** across sessions  
    ✅ **Real Mojo performance** - not Python fallbacks  

    ### Advanced Usage

    Try the decorator approach for cleaner APIs:

    ```python
    from mojo_marimo import mojo
    
    @mojo
    def my_function(n: int) -> int:
        '''Mojo code in docstring'''
        pass
    ```
    """)
    return


@app.cell
def _():
    # Cell for future benchmarking comparison
    return


if __name__ == "__main__":
    app.run()
