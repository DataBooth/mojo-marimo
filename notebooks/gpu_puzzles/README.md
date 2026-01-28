# Mojo GPU puzzles with `py_run_mojo`

This directory contains marimo and Jupyter notebooks plus Mojo source files
for exploring the official Mojo GPU puzzles published at
<https://puzzles.modular.com>.

The puzzles themselves – story, diagrams, and reference solutions – are
hosted and maintained by Modular. This repository **does not** copy that
material. Instead, it provides local, experiment-friendly notebooks that
let you:

- paste or re-type the official puzzle kernels and host drivers,
- iterate on your own implementations, and
- run them via the `py_run_mojo` executor from normal Python tools.

In other words, these notebooks are examples of how to use `py_run_mojo`
(and marimo / Jupyter) as a thin integration layer around an existing
Mojo codebase: you stay inside Python, but still compile and execute
real Mojo GPU programs.

## Layout

Each puzzle lives in its own subdirectory, e.g. `p01/`:

- `p01_hello_threads.py` – marimo notebook for the puzzle.
- `p01_hello_threads.ipynb` – Jupyter notebook variant.
- `mojo/p01_setup.mojo` – setup and definitions (imports, types, constants).
- `mojo/p01_kernel.mojo` – the GPU kernel you edit.
- `mojo/p01_main.mojo` – the host driver `main` function.
- `mojo/p01_*.mojo` – additional variants or saved solutions.

Shared utilities live alongside the puzzle folders:

- `gpu_puzzles_utils_marimo.py` – utilities for marimo notebooks
  (loading fragments, running kernels, saving programs).
- `gpu_puzzles_utils_jupyter.py` – utilities for Jupyter notebooks
  (loading fragments, rich code display, running and saving programs).

To add a new puzzle, create `pNN/` with the same pattern and update the
notebooks to call into the shared utility modules.
