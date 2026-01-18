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
    # Import our compute functions (runs real Mojo code!)
    from compute_wrapper import fibonacci, sum_squares, is_prime, get_mojo_version
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
    fib_slider = mo.ui.slider(
        start=1, 
        stop=30, 
        value=10, 
        label="n:",
        show_value=True
    )
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
    sum_sq_slider = mo.ui.slider(
        start=1,
        stop=100,
        value=10,
        label="n:",
        show_value=True
    )
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
    prime_input = mo.ui.number(
        start=1,
        stop=10000,
        value=17,
        label="Check if prime:"
    )
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

    This notebook uses **`mo_run_mojo`** to execute real Mojo code:

    1. Each function call generates Mojo source code
    2. Code is written to a temporary `.mojo` file
    3. `mojo run` executes the code via subprocess
    4. Output is parsed and returned to marimo

    ### Advantages

    ✅ **No compilation step** - just run Mojo code directly  
    ✅ **Easy debugging** - can echo code and output  
    ✅ **Rapid prototyping** - modify Mojo code on the fly  
    ✅ **Real Mojo performance** - not Python fallbacks  

    ### For Production

    For even better performance, compile to Python extension modules:

    ```bash
    mojo package compute.mojo -o compute_ext
    ```

    This eliminates subprocess overhead and provides native Python integration.
    """)
    return


@app.cell
def _():
    # Cell for future benchmarking comparison
    return


if __name__ == "__main__":
    app.run()
