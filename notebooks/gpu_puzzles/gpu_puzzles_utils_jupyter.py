"""Jupyter utilities for Mojo GPU puzzle notebooks.

These helpers are used by Jupyter-based notebooks for the GPU puzzles.
"""

from pathlib import Path
from typing import Callable, Optional, Tuple

try:  # Used in Jupyter notebooks for rich rendering
    from IPython.display import Markdown, display  # type: ignore[import-untyped]
except Exception:  # pragma: no cover - non-notebook environments
    Markdown = None  # type: ignore[assignment]
    display = None   # type: ignore[assignment]


def load_puzzle_fragments(problem: str) -> Tuple[str, str, str]:
    """Load setup, kernel, and main fragments for a given puzzle.

    Kept in sync with :func:`gpu_puzzles_utils_marimo.load_puzzle_fragments`.
    """

    base = Path(__file__).parent / problem / "mojo"
    setup_path = base / f"{problem}_setup.mojo"
    kernel_path = base / f"{problem}_kernel.mojo"
    main_path = base / f"{problem}_main.mojo"

    setup_code = setup_path.read_text()
    kernel_code = kernel_path.read_text()
    main_code = main_path.read_text()

    return setup_code, kernel_code, main_code


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
    """Print a simple mapping from (block, thread) to linear index."""

    for b in range(num_blocks):
        for t in range(threads_per_block):
            i = b * threads_per_block + t
            print(f"block {b:2d}, thread {t:2d} -> index {i:3d}")


def run_puzzle_program(run_mojo: Callable[[str], Optional[str]], code: str) -> None:
    """Run a full Mojo program for a puzzle and print a simple status."""

    result = run_mojo(code, echo_output=True)

    if result is None:
        print("Execution failed – see compilation/runtime errors above.")
    else:
        print("Execution succeeded!")
        print(f"Execution result (stdout): {result!r}")


def suggest_puzzle_cli_filename(problem: str) -> str:
    """Return a suggested filename for saving a puzzle's Mojo program."""

    return f"{problem}_solution.mojo"


def save_puzzle_program_for_cli(
    problem: str,
    code: str,
    filename: Optional[str] = None,
) -> Path:
    """Save the assembled Mojo program for CLI use.

    If ``filename`` is not provided, a sensible default based on
    :func:`suggest_puzzle_cli_filename` is used.
    """

    base = Path(__file__).parent / problem / "mojo"
    if filename is None:
        filename = suggest_puzzle_cli_filename(problem)

    out_path = base / filename
    out_path.write_text(code)
    print(f"Saved current program to {out_path}")
    print(f"You can run it with: mojo {out_path}")
    return out_path
