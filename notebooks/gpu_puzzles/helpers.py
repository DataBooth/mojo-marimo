"""Helpers for GPU puzzle notebooks.

This module provides utilities that can be reused across the GPU puzzle
notebooks, such as loading the code fragments for a given problem.
"""

from pathlib import Path
from typing import Callable, Optional, Tuple


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