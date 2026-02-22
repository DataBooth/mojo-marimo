# py-run-mojo justfile
# Cross-platform task runner synced with pixi.toml tasks
# Run `just --list` to see all available commands

# Default recipe shows available commands
default:
    @just --list

# Setup and installation
# ----------------------

# Install dependencies with uv
install:
    uv sync --extra dev

# Install dependencies with pixi
install-pixi:
    pixi install

# Setup verification
# ------------------

# Verify Mojo and environment setup
test-setup:
    uv run python scripts/verify_setup.py

# Verify all .mojo files compile successfully
check-mojo-build:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Checking all .mojo files compile..."
    for file in examples/*.mojo; do
        basename="$(basename "$file")"
        echo "Checking $file..."
        # Extension modules (*_ext.mojo) don't have main(), skip build
        if [[ "$basename" == *_ext.mojo ]]; then
            echo "  → Extension module (skipping executable build)"
        else
            # Regular .mojo files - build to verify they compile
            uv run mojo build "$file" -o "/tmp/$(basename "$file" .mojo)" > /dev/null 2>&1 || exit 1
            echo "  ✓ Compiled successfully"
        fi
    done
    echo "✅ All .mojo files validated!"
    rm -f /tmp/{monte_carlo,mandelbrot,examples}

# Interactive notebooks
# ---------------------

# Interactive learning notebook (for newcomers)
learn:
    uv run marimo edit notebooks/interactive_learning.py

# Open decorator pattern notebook
notebook-decorator:
    uv run marimo edit notebooks/pattern_decorator.py

# Open executor pattern notebook
notebook-executor:
    uv run marimo edit notebooks/pattern_executor.py

# Open extension module pattern notebook
notebook-extension:
    uv run marimo edit notebooks/pattern_extension.py

# Monte Carlo Pi estimation notebooks
notebook-mc-decorator:
    uv run marimo edit notebooks/monte_carlo_decorator.py

notebook-mc-executor:
    uv run marimo edit notebooks/monte_carlo_executor.py

notebook-mc-extension:
    uv run marimo edit notebooks/monte_carlo_extension.py

# Mandelbrot set notebooks
notebook-mandelbrot-decorator:
    uv run marimo edit notebooks/mandelbrot_decorator.py

notebook-mandelbrot-executor:
    uv run marimo edit notebooks/mandelbrot_executor.py

notebook-mandelbrot-extension:
    uv run marimo edit notebooks/mandelbrot_extension.py

# GPU puzzle notebooks (marimo)
notebook-gpu-p01-hello-threads:
    uv run marimo edit notebooks/gpu_puzzles/p01/p01_hello_threads.py

notebook-gpu-p02-zip:
    uv run marimo edit notebooks/gpu_puzzles/p02/p02_zip.py

# Open Python vs Mojo benchmark notebook
benchmark:
    uv run marimo edit benchmarks/python_vs_mojo.py

# Open execution approaches benchmark
benchmark-exec:
    uv run marimo edit benchmarks/execution_approaches.py

# Jupyter notebooks
# -----------------

# Launch Jupyter notebook browser in jupyter/ directory
jupyter:
    VIRTUAL_ENV= uv run jupyter notebook notebooks/jupyter/

# Open decorator pattern notebook (Jupyter)
jupyter-decorator:
    VIRTUAL_ENV= uv run jupyter notebook notebooks/jupyter/pattern_decorator.py

# Open executor pattern notebook (Jupyter)
jupyter-executor:
    VIRTUAL_ENV= uv run jupyter notebook notebooks/jupyter/pattern_executor.py

# Monte Carlo notebooks (Jupyter)
jupyter-mc:
    VIRTUAL_ENV= uv run jupyter notebook notebooks/jupyter/monte_carlo_extension.py

jupyter-mc-decorator:             # Monte Carlo decorator notebook (Jupyter)
    VIRTUAL_ENV= uv run jupyter notebook notebooks/jupyter/monte_carlo_decorator.py

jupyter-mc-executor:               # Monte Carlo executor notebook (Jupyter)
    VIRTUAL_ENV= uv run jupyter notebook notebooks/jupyter/monte_carlo_executor.py

# Convert Jupyter .py files to .ipynb format
jupyter-convert:
    #!/usr/bin/env bash
    cd notebooks/jupyter
    for file in *.py; do
        [ -f "$file" ] || continue
        VIRTUAL_ENV= uv run jupytext --to notebook "$file"
        echo "✓ Converted $file → ${file%.py}.ipynb"
    done
    echo "✅ All notebooks converted!"

# Command-line demos
# ------------------

# Run examples module demo
demo-examples:
    VIRTUAL_ENV= uv run python examples/examples.py

# Run decorator demo
demo-decorator:
    VIRTUAL_ENV= uv run python -m py_run_mojo.decorator

# Testing
# -------

# Run all tests
test:
    VIRTUAL_ENV= uv run python -m pytest tests/

# Run all tests with verbose output
test-verbose:
    VIRTUAL_ENV= uv run python -m pytest tests/ -v

# Run tests with coverage report
test-coverage:
    VIRTUAL_ENV= uv run python -m pytest tests/ --cov=src/py_run_mojo --cov-report=term-missing

# Run quick tests (skip slow ones)
test-quick:
    VIRTUAL_ENV= uv run python -m pytest tests/ -m "not slow"

# Code quality
# ------------

# Format code with ruff
format:
    VIRTUAL_ENV= uv run ruff format .

# Lint code with ruff
lint:
    VIRTUAL_ENV= uv run ruff check .

# Fix linting issues automatically
lint-fix:
    VIRTUAL_ENV= uv run ruff check --fix .

# Run type checker
typecheck:
    VIRTUAL_ENV= uv run ty check

# Run all quality checks (format, lint, typecheck)
check: format lint typecheck
    @echo "✅ All quality checks passed!"

# Development
# -----------

# Build and packaging
build:
    VIRTUAL_ENV= uv run hatch build

publish-test:
    VIRTUAL_ENV= uv run hatch publish -r test

publish:
    VIRTUAL_ENV= uv run hatch publish

# Clean up cache and build artifacts
clean:
    rm -rf .pytest_cache
    rm -rf .ruff_cache
    rm -rf __pycache__
    rm -rf **/__pycache__
    rm -rf .coverage
    rm -rf htmlcov
    rm -rf dist
    rm -rf build
    rm -rf *.egg-info

# Clean Mojo cache
clean-mojo-cache:
    rm -rf ~/.mojo_cache/binaries/*
    @echo "✅ Mojo cache cleared"

# Show Mojo cache stats
cache-stats:
    VIRTUAL_ENV= uv run python -c "from py_run_mojo.executor import cache_stats; cache_stats()"

# Project info
# ------------

# Show project info
info:
    @echo "Project: py-run-mojo"
    @echo ""
    @echo "Environment:"
    @VIRTUAL_ENV= uv run python -c "import sys; print(f'  Python: {sys.version}')"
    @VIRTUAL_ENV= uv run python -c "import py_run_mojo; print(f'  Package: {py_run_mojo.__version__}')"
    @echo ""
    @echo "Tools:"
    @echo "  UV: $(uv --version)"
    @VIRTUAL_ENV= uv run mojo --version 2>/dev/null || echo "  Mojo: not found (install with: modular install mojo)"

# Show installed packages
list-packages:
    VIRTUAL_ENV= uv pip list

# Verify published package from PyPI using uv in a fresh temporary environment
verify-pypi:
    #!/usr/bin/env bash
    set -euo pipefail
    ENV_DIR="$(mktemp -d /tmp/py-run-mojo-prod-XXXXXX)"
    echo "▶ Creating fresh uv virtualenv at $ENV_DIR"
    uv venv "$ENV_DIR"
    echo "▶ Activating virtualenv"
    # shellcheck disable=SC1090
    source "$ENV_DIR/bin/activate"
    echo "▶ Installing py-run-mojo from PyPI via uv"
    uv pip install --index-url https://pypi.org/simple py-run-mojo
    echo "▶ Verifying installed package"
    python - <<'EOF'
    import py_run_mojo

    print("installed_version =", py_run_mojo.__version__)

    try:
        from py_run_mojo import get_mojo_version
        print("mojo_version    =", get_mojo_version())
    except Exception as e:
        print("get_mojo_version failed (this is OK if mojo isn't installed):", e)
    EOF
    echo "✅ PyPI package verification finished"

# CI/CD simulation
# ----------------

# Run CI checks locally
ci: check test
    @echo "✅ CI checks passed!"
