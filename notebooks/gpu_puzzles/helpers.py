"""Helpers for GPU puzzle notebooks.

This module provides utilities that can be reused across the GPU puzzle
notebooks, such as loading the code fragments for a given problem.
"""

from pathlib import Path
from typing import Callable, Optional, Tuple

try:  # Used in Jupyter notebooks for rich rendering
    from IPython.display import Markdown, display  # type: ignore[import-untyped]
except Exception:  # pragma: no cover - non-notebook environments
    Markdown = None  # type: ignore[assignment]
    display = None   # type: ignore[assignment]


def load_problem_code(problem: str) -> Tuple[str, str, str]:
    """Load setup, kernel, and main segments for a given puzzle.

    The ``problem`` name should be of the form ``"p01"``, ``"p02"``, etc.
    This helper expects the following files under ``notebooks/gpu_puzzles``::

        {problem}_setup_code.mojo
        {problem}_kernel_code.mojo
        {problem}_main_code.mojo

    Returns:
        A tuple ``(setup_code, kernel_code, main_code)``.
    """
    base = Path(__file__).parent
    setup_path = base / f"{problem}_setup_code.mojo"
    kernel_path = base / f"{problem}_kernel_code.mojo"
    main_path = base / f"{problem}_main_code.mojo"

    setup_code = setup_path.read_text()
    kernel_code = kernel_path.read_text()
    main_code = main_path.read_text()

    return setup_code, kernel_code, main_code


def run_mojo_code(
    mo,
    run_mojo: Callable[[str], Optional[str]],
    code: str,
    label: str = "Execution result",
) -> None:
    """Run Mojo code with a given run_mojo function and show a callout."""
    result = run_mojo(code, echo_output=True)

    if result is None:
        mo.callout(
            "Execution failed – see compilation/runtime errors above.",
            kind="danger",
        )
    else:
        mo.callout(f"{label} (see printed output above).", kind="success")
        mo.md(f"Execution result (stdout): `{result}`")


def save_problem_code(problem: str, code: str) -> Path:
    """Save edited code for a problem to a `.mojo` file and return the path."""
    base = Path(__file__).parent
    out_path = base / f"{problem}_edited.mojo"
    out_path.write_text(code)
    return out_path


def show_mojo_block(title: str, code: str, language: str = "mojo") -> None:
    """Render a titled fenced code block in a Jupyter notebook.

    Falls back to a plain ``print`` if IPython.display is unavailable.
    """
    if Markdown is None or display is None:
        print(f"=== {title} ===")
        print(code)
        return

    md = f"### {title}\n\n```{language}\n{code}\n```"
    display(Markdown(md))


def visualise_threads(num_blocks: int, threads_per_block: int) -> None:
    """Print a simple mapping from (block, thread) to linear index.

    Useful in both marimo and Jupyter notebooks for building GPU intuition.
    """
    for b in range(num_blocks):
        for t in range(threads_per_block):
            i = b * threads_per_block + t
            print(f"block {b:2d}, thread {t:2d} -> index {i:3d}")


def run_puzzle_program(run_mojo: Callable[[str], Optional[str]], code: str) -> None:
    """Run a full Mojo program for a puzzle and print a simple status.

    This is a Jupyter-friendly variant of :func:`run_mojo_code` that does not
    depend on marimo; it just prints to standard output.
    """
    result = run_mojo(code, echo_output=True)

    if result is None:
        print("Execution failed – see compilation/runtime errors above.")
    else:
        print("Execution succeeded!")
        print(f"Execution result (stdout): {result!r}")


def save_puzzle_program_for_cli(
    problem_id: str,
    code: str,
    suffix: str = "_jupy",
) -> Path:
    """Save the assembled Mojo program for CLI use.

    A small wrapper around :func:`save_problem_code` that appends a suffix
    (default ``"_jupy"``) to the puzzle id so Jupyter and marimo do not
    overwrite each other's ``*.mojo`` files.
    """
    jupy_problem_id = f"{problem_id}{suffix}"
    return save_problem_code(jupy_problem_id, code)
