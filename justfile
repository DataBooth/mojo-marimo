# mojo-marimo justfile
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

# Open benchmark notebook
benchmark:
    uv run marimo edit notebooks/benchmark.py

# Command-line demos
# ------------------

# Run examples module demo
demo-examples:
    uv run python examples/examples.py

# Run decorator demo
demo-decorator:
    uv run python -m mojo_marimo.decorator

# Testing
# -------

# Run all tests
test:
    uv run pytest tests/

# Run all tests with verbose output
test-verbose:
    uv run pytest tests/ -v

# Run tests with coverage report
test-coverage:
    uv run pytest tests/ --cov=src/mojo_marimo --cov-report=term-missing

# Run quick tests (skip slow ones)
test-quick:
    uv run pytest tests/ -m "not slow"

# Code quality
# ------------

# Format code with ruff
format:
    uv run ruff format .

# Lint code with ruff
lint:
    uv run ruff check .

# Fix linting issues automatically
lint-fix:
    uv run ruff check --fix .

# Run type checker
typecheck:
    uv run ty check

# Run all quality checks (format, lint, typecheck)
check: format lint typecheck
    @echo "✅ All quality checks passed!"

# Development
# -----------

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
    uv run python -c "from mojo_marimo.executor import cache_stats; cache_stats()"

# Project info
# ------------

# Show project info
info:
    @echo "Project: mojo-marimo"
    @echo ""
    @echo "Environment:"
    @uv run python -c "import sys; print(f'  Python: {sys.version}')"
    @uv run python -c "import mojo_marimo; print(f'  Package: {mojo_marimo.__version__}')"
    @echo ""
    @echo "Tools:"
    @echo "  UV: $(uv --version)"
    @uv run mojo --version 2>/dev/null || echo "  Mojo: not found (install with: modular install mojo)"

# Show installed packages
list-packages:
    uv pip list

# CI/CD simulation
# ----------------

# Run CI checks locally
ci: check test
    @echo "✅ CI checks passed!"
