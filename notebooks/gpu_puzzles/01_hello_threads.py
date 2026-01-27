"""GPU Puzzle 01–02: Hello Threads (skeleton notebook).

This notebook is a *scaffold* for the first Mojo GPU puzzles.
It intentionally does **not** include the original puzzle text or
solution code. Use it alongside https://puzzles.modular.com.
"""

import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _(mo):
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
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Setup / Imports

    - `py_run_mojo` package
    - Local notebook `helpers` functions
    """)
    return


@app.cell
def _():
    import marimo as mo
    from helpers import load_problem_code, save_problem_code, run_mojo_code
    from py_run_mojo import run_mojo, get_mojo_version
    problem_id = "p01"
    return (
        get_mojo_version,
        load_problem_code,
        mo,
        problem_id,
        run_mojo,
        run_mojo_code,
        save_problem_code,
    )


@app.cell
def _(load_problem_code, problem_id):
    # Load the three code segments (setup, kernel, main) for puzzle p01 from .mojo files

    mojo_setup_code, mojo_kernel_code, mojo_main_code = load_problem_code(problem_id)
    return mojo_kernel_code, mojo_main_code, mojo_setup_code


@app.cell
def _(get_mojo_version, mo):
    mo.md(f"""
    ## 2. Environment & version
    Mojo version: `{get_mojo_version()}`
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Mojo code structure

    We split the puzzle's Mojo code into three logical pieces:

    - **i. Setup and definitions** – imports, compile-time constants, and types.
    - **ii. Kernel** – the GPU kernel that runs on each thread (in this example `add_10`)
    - **iii. Host `main`** – the driver that allocates buffers, launches the
      kernel, and checks results.

    In this notebook you *edit the kernel body*; setup and host code
    are shown read-only for context.
    """)
    return


@app.cell
def _(mo, mojo_setup_code):
    mo.ui.code_editor(
                value=mojo_setup_code,
                label="### i. Setup and definitions",
                theme="dark",
                language="python",
                disabled=True,
                min_height=140,
            )
    return


@app.cell
def _(mo, mojo_main_code):
    mo.ui.code_editor(
                label = "### iii. Host driver: `main`",
                value=mojo_main_code,
                theme="dark",
                language="python",
                disabled=True,
                min_height=260,
            )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Edit the kernel to solve the puzzle
    """)
    return


@app.cell
def _(mo, mojo_kernel_code):
    # Interactive editor for the kernel

    kernel_editor = mo.ui.code_editor(
        value=mojo_kernel_code,
        theme="dark",
        language="python",
        label="### Kernel: (**FILL ME IN**)",
        min_height=220,
    )
    return (kernel_editor,)


@app.cell
def _(kernel_editor):
    kernel_editor
    return


@app.cell
def _(mo):
    mo.md("""
    Tips:

    - Use `i = thread_idx.x` to pick the current element.
    - Read from `a` and write to `output`.
    - Make sure you don't go out of bounds when you experiment.
    """)
    return


@app.cell
def _(kernel_editor, mo, mojo_main_code, mojo_setup_code):

    mojo_code = "\n\n".join(
        [
            mojo_setup_code,
            kernel_editor.value,
            mojo_main_code,
        ]
    )

    # Optional: inspect the full Mojo program that will be sent to `run_mojo`.
    # You can copy-paste this into a standalone `.mojo` file if you want to
    # run it from the command line.
    try:
        expander = mo.expander("Show entire Mojo program")
        with expander:
            mo.ui.code_editor(
                value=mojo_code,
                theme="dark",
                language="python",
                disabled=True,
                min_height=260,
            )
    except Exception:
        # Fallback if this marimo version does not have `expander`.
        mo.ui.code_editor(
            value=mojo_code,
            theme="dark",
            language="python",
            disabled=True,
            min_height=260,
        )
    return (mojo_code,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Run and inspect output

    Click **Run kernel** to compile and execute the Mojo program. Any `print`
    output from `main()` (including the puzzle's own assertions) will appear
    below.
    """)
    return


@app.cell
def _(mo, mojo_code, problem_id, save_problem_code):
    """Save the current Mojo program to a `.mojo` file for use on the CLI."""

    def save_code() -> None:
        path = save_problem_code(problem_id, mojo_code)
        mo.callout(
            f"Saved current kernel to `{path}`. You can run it with `mojo {path}`.",
            kind="info",
        )

    save_button = mo.ui.button(
        label="Save Mojo file for this puzzle",
        on_click=lambda _: save_code(),
    )
    mo.hstack([save_button], justify="center")
    return


@app.cell
def _(mo, mojo_code, run_mojo, run_mojo_code):
    run_kernel_button = mo.ui.button(
        label="Run kernel...",
        on_click=lambda _: run_mojo_code(mo, run_mojo, mojo_code, label="Kernel run"),
    )
    mo.hstack([run_kernel_button], justify="center")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
