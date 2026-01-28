"""Marimo utilities for Mojo GPU puzzle notebooks.

These helpers are used by marimo-based notebooks under ``notebooks/gpu_puzzles``.
"""

from pathlib import Path
from typing import Callable, Optional, Tuple


def load_puzzle_fragments(problem: str) -> Tuple[str, str, str]:
    """Load setup, kernel, and main fragments for a given puzzle.

    ``problem`` should be an identifier like ``"p01"``.

    Files are expected under ``notebooks/gpu_puzzles/<problem>/`` with
    the following names::

        <problem>_setup.mojo
        <problem>_kernel.mojo
        <problem>_main.mojo

    Returns
    -------
    (setup_code, kernel_code, main_code)
    """

    base = Path(__file__).parent / problem / "mojo"
    setup_path = base / f"{problem}_setup.mojo"
    kernel_path = base / f"{problem}_kernel.mojo"
    main_path = base / f"{problem}_main.mojo"

    setup_code = setup_path.read_text()
    kernel_code = kernel_path.read_text()
    main_code = main_path.read_text()

    return setup_code, kernel_code, main_code


def run_puzzle_with_marimo(
    mo,
    run_mojo: Callable[[str], Optional[str]],
    code: str,
    label: str = "Execution result",
) -> None:
    """Run Mojo code from a marimo notebook and show a callout.

    This mirrors the behaviour used in the original ``helpers.run_mojo_code``.
    """

    result = run_mojo(code, echo_output=True)

    if result is None:
        mo.callout(
            "Execution failed – see compilation/runtime errors above.",
            kind="danger",
        )
    else:
        mo.callout(f"{label} (see printed output above).", kind="success")
        mo.md(f"Execution result (stdout): `{result}`")


def suggest_puzzle_cli_filename(problem: str) -> str:
    """Return a suggested filename for saving a puzzle's Mojo program."""

    return f"{problem}_solution.mojo"


def save_puzzle_program(
    problem: str,
    code: str,
    filename: Optional[str] = None,
) -> Path:
    """Save edited code for a puzzle to a ``.mojo`` file and return the path.

    If ``filename`` is not provided, :func:`suggest_puzzle_cli_filename` is
    used to generate one inside the puzzle's directory.
    """

    base = Path(__file__).parent / problem / "mojo"
    if filename is None:
        filename = suggest_puzzle_cli_filename(problem)

    out_path = base / filename
    out_path.write_text(code)
    return out_path
