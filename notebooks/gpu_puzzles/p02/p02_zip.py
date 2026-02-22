"""GPU Puzzle 02: Zip (marimo notebook scaffold).

Use alongside https://puzzles.modular.com/puzzle_02/puzzle_02.html.
"""

import marimo

from gpu_puzzles_utils_marimo import (
    load_puzzle_fragments,
    run_puzzle_with_marimo,
    save_puzzle_program,
)
from py_run_mojo import run_mojo, get_mojo_version

app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # GPU Puzzle 02: Zip

    This notebook is designed to be used **with** the official Mojo GPU
    Puzzles at https://puzzles.modular.com.

    - Read the puzzle description on the official site.
    - Paste or re-type the relevant Mojo kernel and driver code into the
      code cells below.
    - Use the controls here to experiment with different inputs.

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
    - GPU puzzle utilities for loading/saving/running code
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

    problem_id = "p02"
    return (
        get_mojo_version,
        load_puzzle_fragments,
        mo,
        problem_id,
        run_mojo,
        run_puzzle_with_marimo,
        save_puzzle_program,
    )


@app.cell
def _(get_mojo_version, mo):
    mo.md(f"""
    ## 2. Environment & version
    Mojo version: `{get_mojo_version()}`
    """)
    return


@app.cell
def _(load_puzzle_fragments, problem_id):
    # Load the three code segments (setup, kernel, main) for this puzzle

    setup_code, kernel_code, main_code = load_puzzle_fragments(problem_id)
    return setup_code, kernel_code, main_code


@app.cell
def _(mo, setup_code):
    mo.md("""### Setup and definitions (read-only)""")
    mo.ui.code_editor(
        value=setup_code,
        label="Setup",
        theme="dark",
        language="python",
        disabled=True,
        min_height=140,
    )
    return


@app.cell
def _(mo, main_code):
    mo.md("""### Host driver `main` (read-only)""")
    mo.ui.code_editor(
        value=main_code,
        label="Host main",
        theme="dark",
        language="python",
        disabled=True,
        min_height=260,
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Edit the kernel to solve the puzzle
    """)
    return


@app.cell
def _(mo, kernel_code):
    kernel_editor = mo.ui.code_editor(
        value=kernel_code,
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
    - Read from `a` and `b`, write to `output`.
    - Make sure you do not go out of bounds when you experiment.
    """)
    return


@app.cell
def _(kernel_editor, mo, setup_code, main_code):
    mojo_code = "\n\n".join([
        setup_code,
        kernel_editor.value,
        main_code,
    ])

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
def _(mo, mojo_code, problem_id, save_puzzle_program):
    """Save the current Mojo program to a `.mojo` file for use on the CLI."""

    def save_code() -> None:
        path = save_puzzle_program(problem_id, mojo_code)
        mo.callout(
            f"Saved current kernel to `{path}`. You can run it with `mojo {path}`.",
            kind="info",
        )

    save_button = mo.ui.button(
        label="Save Mojo file for this puzzle",
        on_click=lambda _: save_code(),
    )
    save_button
    return


@app.cell
def _(mo, mojo_code, run_mojo, run_puzzle_with_marimo):
    run_kernel_button = mo.ui.button(
        label="Run kernel...",
        on_click=lambda _: run_puzzle_with_marimo(mo, run_mojo, mojo_code, label="Kernel run"),
    )
    mo.hstack([run_kernel_button], justify="center")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
