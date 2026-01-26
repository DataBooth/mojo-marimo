"""GPU Puzzles with py-run-mojo - index notebook.

This marimo notebook provides an overview and entry point for the
Mojo GPU puzzles hosted at https://puzzles.modular.com.

It does NOT copy puzzle text or solutions. Instead, it links to the
official site and provides interactive scaffolding for exploration.
"""

import marimo

app = marimo.App(width="large")


@app.cell
def _():
    import marimo as mo

    mo.md(r"""
    # Mojo GPU Puzzles with `py-run-mojo`

    Interactive marimo notebooks that wrap the official Mojo GPU Puzzles
    in a reactive, experiment-friendly environment.

    - Uses `py_run_mojo.run_mojo` under the hood
    - Keeps the original puzzles on https://puzzles.modular.com as the
      source of truth
    - Provides sliders, visualisations, and timing helpers for learning

    ## Notebook layout

    Each puzzle (or small group of related puzzles) lives in its own
    notebook under `notebooks/gpu_puzzles/`, following this pattern:

    - `NN_short_title.py` (zero-padded puzzle number)
    - Header with puzzle link & summary
    - Mojo kernel + driver code cells (you paste or adapt from the
      official puzzle repo)
    - Interactive controls (array size, block size, etc.)
    - Output + simple plots where relevant

    This index notebook is a simple directory and progress view.
    """)
    return (mo,)


@app.cell
def _(mo):
    import pathlib

    base = pathlib.Path(__file__).parent
    puzzle_files = sorted(p for p in base.glob("[0-9][0-9]_*.py") if p.name != "index.py")

    rows = []
    for p in puzzle_files:
        number, rest = p.stem.split("_", 1)
        title = rest.replace("_", " ")
        rows.append((number, title, p.name))

    if not rows:
        mo.md("No GPU puzzle notebooks found yet. Start by creating `01_hello_threads.py`.")
    else:
        lines = ["| # | Notebook | File |", "|---|----------|------|"]
        for num, title, fname in rows:
            lines.append(f"| {num} | {title} | `{fname}` |")
        mo.md("\n".join(lines))

    return


if __name__ == "__main__":
    app.run()
