"""GPU Puzzle 01–02: Hello Threads (skeleton notebook).

This notebook is a *scaffold* for the first Mojo GPU puzzles.
It intentionally does **not** include the original puzzle text or
solution code. Use it alongside https://puzzles.modular.com.
"""

import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(r"""
    # GPU Puzzles 01–02: Hello Threads

    This notebook is designed to be used **with** the official Mojo GPU
    Puzzles at https://puzzles.modular.com.

    - Read the puzzle description on the official site.
    - Paste or re-type the relevant Mojo kernel and driver code into the
      code cells below.
    - Use the controls here to experiment with different grid/block
      configurations and inputs.

    > **Note:** This repository and notebook are not affiliated with
    > Modular. They are just an educational wrapper around the public
    > puzzles.
    """)
    return (mo,)


@app.cell
def _():
    import marimo as mo

    mo.md(r"""
    ## 1. Environment & version

    We use `py_run_mojo.run_mojo` to compile and execute Mojo code from
    Python. This assumes the `mojo` CLI is available on your PATH.
    """)
    return (mo,)


@app.cell
def _():
    from py_run_mojo import get_mojo_version
    from marimo import md

    md(f"Mojo version: `{get_mojo_version()}`")
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np

    # Controls for simple experiments; feel free to extend.
    n = mo.ui.slider(16, 4096, step=16, label="Number of elements")

    mo.md(r"""
    ## 2. Parameters

    Use the slider to control the size of the input array. You can also
    add more controls for block size, grid dimensions, etc.
    """)

    mo.display(n)

    # Example host data (you can adapt to the puzzle's semantics)
    host_array = np.arange(n.value, dtype=np.float32)

    return host_array, n


@app.cell
def _(host_array, n):
    import marimo as mo

    mo.md(r"""
    ## 3. Mojo kernel (paste or write here)

    Paste your Mojo kernel + driver code from the official GPU puzzle.
    For example, you might have a kernel that writes the thread index
    into an output array.

    Use `{{n}}` as a placeholder for `n` if you want to substitute the
    Python value into the Mojo code string.
    """)

    # TODO: replace this placeholder with your real Mojo code
    mojo_code = f"""
    # Paste your Mojo kernel and main() here.
    # Example shape (this is NOT the official solution):
    #
    # @kernel
    # fn hello_threads(out: ptr[f32]):
    #     let i = ...
    #
    # fn main():
    #     # allocate, launch, print
    #     ...
    
    fn main():
        print("Hello from placeholder main(); replace me with puzzle code.")
    """

    return mojo_code


@app.cell
def _(host_array, mojo_code, n):
    import marimo as mo
    from py_run_mojo import run_mojo

    mo.md(r"""
    ## 4. Run and inspect output

    When you are happy with your Mojo code, run this cell to execute it.
    Any `print` output from `main()` will appear below.
    """)

    result = run_mojo(mojo_code)

    mo.md(f"Execution result (stdout): `{result}`")

    return


if __name__ == "__main__":
    app.run()
