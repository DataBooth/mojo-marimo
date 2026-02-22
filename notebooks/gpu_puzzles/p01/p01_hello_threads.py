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
    # Mojo 🔥 GPU Puzzles: 01 - Hello Threads

    This notebook is designed to be used **with** the official Mojo GPU
    Puzzles by Modular at https://puzzles.modular.com.

    - Read the puzzle description on the official site.
    - The relevant Mojo setup (read only), kernel and driver (read only) code are provided in the code cells below.
    - **Edit the kernel code to complete the GPU puzzle.**

    > **Note:** This repository and notebook are not affiliated with
    > Modular. They are just an educational wrapper around the public puzzles.
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
    import sys
    from pathlib import Path

    # Ensure the gpu_puzzles utils module is importable when running this notebook.
    ROOT = Path(__file__).resolve().parent.parent  # .../notebooks/gpu_puzzles
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))

    from gpu_puzzles_utils_marimo import (
        load_puzzle_fragments,
        run_puzzle_with_marimo,
        save_puzzle_program,
    )
    from py_run_mojo import run_mojo, get_mojo_version
    return (
        get_mojo_version,
        load_puzzle_fragments,
        mo,
        run_mojo,
        run_puzzle_with_marimo,
        save_puzzle_program,
    )


@app.cell
def _():
    problem_id = "p01"
    return (problem_id,)


@app.cell
def _(load_puzzle_fragments, problem_id):
    # Load the three code segments (setup, kernel, main) for this puzzle from .mojo files

    setup_code, kernel_code, main_code = load_puzzle_fragments(problem_id)
    return kernel_code, main_code, setup_code


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
def _(mo, setup_code):
    mo.ui.code_editor(
                value=setup_code,
                label="### i. Setup and definitions",
                theme="dark",
                language="python",
                disabled=True,
                min_height=140,
            )
    return


@app.cell
def _(main_code, mo):
    mo.ui.code_editor(
                label = "### iii. Host driver: `main`",
                value=main_code,
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

    Tips:
    - Use `i = thread_idx.x` to pick the current element.
    - Read from `a` and write to `output`.
    - Make sure you don't go out of bounds when you experiment.
    """)
    return


@app.cell
def _(kernel_code, mo):
    # Interactive editor for the kernel

    kernel_code_editor = mo.ui.code_editor(
        value=kernel_code,
        theme="dark",
        language="python",
        label="### Kernel: (Make your edits here to **FILL ME IN**)",
        min_height=220,
    )
    return (kernel_code_editor,)


@app.cell
def _(kernel_code_editor):
    kernel_code_editor
    return


@app.cell
def _(kernel_code_editor, main_code, setup_code):
    all_code = "\n\n".join(
        [
            setup_code,
            kernel_code_editor.value,
            main_code,
        ]
    )
    return (all_code,)


@app.cell
def _(all_code, mo):
    mo.accordion({"**Show/hide entire program**": mo.ui.code_editor(
            value=all_code,
            theme="dark",
            language="python",
            disabled=True,
            min_height=260,
    )})
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Save, Run and inspect output

    Optionally click Save and then **Run kernel** to compile and execute the Mojo program. Any `print`
    output from `main()` (including the puzzle's own assertions) will appear below.
    """)
    return


@app.cell
def _(all_code, mo, problem_id, save_puzzle_program):
    """Save the current Mojo program to a `.mojo` file for use on the CLI.

    Run this cell after editing the kernel to write out a self-contained
    `.mojo` file for the puzzle.
    """

    path = save_puzzle_program(problem_id, all_code)
    info = mo.callout(
        f"Saved current kernel to `{path}`. You can run it in the repo with `mojo {path}`.",
        kind="info",
    )
    name_line = mo.md(f"**Saved file:** `{path.name}`")
    return (name_line,)


@app.cell
def _(name_line):
    name_line
    return


@app.cell
def _(all_code, mo, run_mojo, run_puzzle_with_marimo):
    """Run the current Mojo program and display the result.

    This cell uses `run_puzzle_with_marimo`, which will compile/execute the
    program and show a callout indicating success or failure.
    """

    components = run_puzzle_with_marimo(mo, run_mojo, all_code, label="Kernel run")
    return (components,)


@app.cell
def _(components):
    components
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
