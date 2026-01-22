# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Environment and tooling

- Python 3.12–3.14, managed with **uv** (preferred). The project is configured via `pyproject.toml`.
- Mojo is used via the **`mojo` CLI**; many tests and the executor require `mojo` to be available on `PATH`.
- A `justfile` mirrors the main development workflows; prefer `just` where available, otherwise use the underlying `uv` commands.
- Pixi is supported as an alternative, but you should default to `uv` for environment and dependency management.
- Documentation and comments should use **Australian English** (see `docs/project/CONTRIBUTING.md`).

### Verifying Mojo setup

Use these before running tests or notebooks that execute Mojo code:

```bash
# Using uv directly
uv sync --extra dev
uv run python scripts/verify_setup.py

# Or via just
just install          # uv sync --extra dev
just test-setup       # runs scripts/verify_setup.py under uv
```

If `scripts/verify_setup.py` reports that `mojo` is not on `PATH`, follow its printed instructions to install Mojo and update `PATH` before proceeding.

## Common commands

### Installation and environment

```bash
# Install all dependencies (including Mojo) with uv
uv sync --extra dev

# Show all available just recipes
just --list
```

### Running tests

The test suite is in `tests/` and configured via `[tool.pytest.ini_options]` in `pyproject.toml`.

```bash
# Run the full test suite
just test              # uv run pytest tests/

# Run with coverage summary
just test-coverage     # uv run pytest tests/ --cov=src/py_run_mojo --cov-report=term-missing

# Quick tests (skips tests marked slow)
just test-quick        # uv run pytest tests/ -m "not slow"

# Directly with uv
uv run pytest tests/
```

Run a **single test file or test case** with standard pytest selection:

```bash
# Single file
uv run pytest tests/test_decorator.py

# Single test function
uv run pytest tests/test_decorator.py::test_decorator_basic

# Single parametrised test case
uv run pytest tests/test_executor.py::test_factorial_computation[5-120]
```

Note: `conftest.py` performs a Mojo availability check and will **skip all tests** if the `mojo` CLI is not found on `PATH`.

### Code quality (formatting, linting, type checking)

These are wired through `just` and backed by `ruff` and `ty` (see `pyproject.toml` and `docs/project/CONTRIBUTING.md`).

```bash
# Run all quality checks (format, lint, typecheck)
just check             # format + lint + typecheck

# Individual commands via just
just format            # uv run ruff format .
just lint              # uv run ruff check .
just lint-fix          # uv run ruff check --fix .
just typecheck         # uv run ty check

# Directly with uv
uv run ruff format .
uv run ruff check .
uv run ty check
```

### Notebooks and interactive demos

This project ships both marimo and Jupyter variants of the examples.

```bash
# marimo notebooks (preferred entry points)
just learn                    # interactive_learning.py
just notebook-decorator       # notebooks/pattern_decorator.py
just notebook-executor        # notebooks/pattern_executor.py
just notebook-extension       # notebooks/pattern_extension.py

# Monte Carlo and Mandelbrot marimo notebooks
just notebook-mc-decorator
just notebook-mc-executor
just notebook-mc-extension
just notebook-mandelbrot-decorator
just notebook-mandelbrot-executor
just notebook-mandelbrot-extension

# Benchmarks (marimo)
just benchmark                # benchmarks/python_vs_mojo.py
just benchmark-exec           # benchmarks/execution_approaches.py

# Jupyter notebooks (py + ipynb via jupytext)
just jupyter                  # opens notebooks/jupyter/
just jupyter-decorator
just jupyter-executor
just jupyter-mc

# Convert Jupyter-style .py to .ipynb
just jupyter-convert
```

All of the above are implemented in terms of `uv run ...` commands; if needed, inspect `justfile` for the exact underlying invocation.

### CLI demos and cache management

```bash
# Command-line demos
just demo-examples            # uv run python examples/examples.py
just demo-decorator           # uv run python -m py_run_mojo.decorator

# Mojo cache utilities
just clean-mojo-cache         # rm -rf ~/.mojo_cache/binaries/*
just cache-stats              # uv run python -c "from py_run_mojo.executor import cache_stats; cache_stats()"

# Project / environment info
just info                     # prints Python, package version, Mojo version, etc.

# Simulate CI locally (tests + checks)
just ci                       # equivalent to just check && just test
```

## High-level architecture

### Core package: `src/py_run_mojo`

The `py_run_mojo` package is deliberately small and focused; it exposes three main capabilities via `__init__.py`:

- `py_run_mojo.executor` – compilation and cached execution of Mojo code.
- `py_run_mojo.decorator` – a Python decorator that turns a function docstring into Mojo source and executes it via the executor.
- `py_run_mojo.validator` – lightweight static validation and hinting for common Mojo errors before invoking the compiler.

`__init__.py` defines public metadata (`__version__`, `__author__`, etc.) and re-exports the main API surface:

- `run_mojo`, `clear_cache`, `cache_stats`, `get_mojo_version`
- `mojo` (the decorator)
- `validate_mojo_code`, `get_validation_hint`

Future agents should import from the top-level `py_run_mojo` package unless they explicitly need internal details.

#### Executor

`executor.py` is the core execution engine:

- Accepts either a **Mojo source string** or a **path to a `.mojo` file`** via `run_mojo(source, ...)`.
- Normalises inline code with `textwrap.dedent` so triple-quoted, indented strings work reliably in Python.
- Validates source using `validator.validate_mojo_code` before compilation; on failure it prints an error and an optional hint from `get_validation_hint` and returns `None`.
- Computes a cache key as a SHA256 hash of the final Mojo source and stores compiled binaries under `~/.mojo_cache/binaries/`.
- Uses `mojo build <tempfile.mojo> -o <cached_binary>` via `subprocess.run` to compile, then executes the resulting binary directly.
- Provides `clear_cache()` and `cache_stats()` helpers which operate purely on the cache directory and print human-friendly summaries.
- `get_mojo_version()` shells out to `mojo --version` once (memoised with `functools.cache`).

Key behavioural points for new code:

- `run_mojo` returns the **stdout text** (stripped) or `None` on error; it never raises for normal compile/runtime failures but logs them to stdout/stderr.
- `echo_code` and `echo_output` flags are useful for debugging but should generally be left `False` in library code and tests unless diagnosing an issue.
- `use_cache=False` forces recompilation and bypasses the binary cache; tests rely on `clear_cache()` plus repeated `run_mojo` calls to exercise both cold and warm paths.

#### Decorator

`decorator.py` implements the `@mojo` decorator and a few example functions:

- The decorator:
  - Captures the wrapped function's **docstring** as a Mojo code template.
  - Uses `inspect.signature` to bind call arguments and performs **string substitution** on `{{param_name}}` placeholders in the Mojo template.
  - Calls `run_mojo(..., use_cache=True)` so that the underlying Mojo binary is cached by source hash.
  - Converts the string result from `run_mojo` into `int`, `bool`, or `float` based on the function's **return annotation**; otherwise returns the raw string (or `None`).
- The module defines sample decorated functions (`fibonacci`, `sum_squares`, `is_prime`) and a `__main__` block that prints basic results and cache warm-ups; this is what `just demo-decorator` exercises.

When adding new decorated functions, follow the existing pattern:

- Ensure docstrings contain valid Mojo with a `fn main()` entry point.
- Use `{{param}}` placeholders for argument substitution.
- Provide an explicit return type annotation to get proper conversion.

#### Validator

`validator.py` provides best-effort static checks on Mojo source before invoking the compiler:

- Ensures code is non-empty and that there is either `fn main()` or `def main()` (required for executables).
- Detects mixed tabs/spaces and obvious file-scope statements that should be inside a function (e.g. `var`, `return`, `if` at top level).
- Enforces that `fn`/`def` declarations end with a colon.
- Flags common Python-ism mistakes in Mojo (e.g. `int`/`str`/`bool` instead of `Int`/`String`/`Bool`, `print` without parentheses, `range 10` without parentheses).
- `get_validation_hint(error_msg)` maps known error substrings to short, human-readable remediation snippets used by `executor.run_mojo`.

The validator is intentionally conservative and string-based; avoid making it too strict unless tests are updated to reflect the new behaviour.

## Tests and quality gates

The test suite is organised around the three core concerns:

- **Environment and fixtures** (`tests/conftest.py`)
  - Globally checks `mojo --version` and skips the suite when Mojo is unavailable.
  - Provides small Mojo code fixtures used across tests.

- **Decorator behaviour** (`tests/test_decorator.py`)
  - Validates parameter substitution, type conversion, caching semantics, function metadata preservation, and more complex implementations like Fibonacci and prime checking.

- **Executor behaviour** (`tests/test_executor.py`)
  - Covers inline source vs file-based execution, cache hits/misses, error handling for invalid code and empty source, and a parametrised factorial example.

- **Package wiring** (`tests/test_imports.py`)
  - Asserts that the package metadata and `__all__` exports are correct and that the top-level API is importable.

- **Reference Mojo examples** (`tests/test_reference_examples.py`)
  - Discovers all `.mojo` files in `examples/reference/` and asserts that each at least compiles and runs without returning `None`.

- **Validator coverage** (`tests/test_validator_errors.py`)
  - Ensures the validator catches and hints on the main error classes it is designed to handle.

When modifying executor/decorator/validator behaviour, update the corresponding tests first; many subtle expectations (e.g. how `None` is used to signal failure) are encoded there.

## Examples, notebooks, and benchmarks

Beyond the core package, several auxiliary directories demonstrate and exercise the patterns:

- `examples/`
  - Python and Mojo reference implementations used for CLI demos and integration tests.
  - `examples.py` wraps common algorithms and is used by `scripts/verify_setup.py` and `just demo-examples`.

- `benchmarks/`
  - Side-by-side Python vs Mojo implementations and marimo notebooks for performance comparison (see `benchmarks/README.md`).
  - Focused on Fibonacci, sum of squares, prime testing, factorial, GCD, and counting primes.

- `notebooks/`
  - marimo notebooks showcasing the decorator, executor, and extension-module patterns, with interactive UI elements.

- `notebooks/jupyter/`
  - Jupyter-style `.py` notebooks with `# %%` cells plus generated `.ipynb` files; these avoid marimo-specific APIs and are suitable for VSCode, JupyterLab, etc.

- `docs/project/`
  - Higher-level design and implementation notes (`README.md`, `SUMMARY.md`).
  - Contribution guidelines (`CONTRIBUTING.md`) including tooling expectations and language conventions.

Future agents making architectural changes should consult both the root `README.md` and `docs/project/SUMMARY.md` to ensure new work aligns with the existing three-pattern model (uncached execution, cached binaries, decorator) and the cache design centred on `~/.mojo_cache/binaries/`.
