# Migration from mojo-fireplace

This document summarizes the migration of the marimo+Mojo integration from the `mojo-fireplace` repository to its own standalone repository `mojo-marimo`.

## Migration Date

2026-01-18

## Source

- **Original location**: `/Users/mjboothaus/code/github/databooth/mojo-fireplace/src/marimo_mojo/`
- **Original repository**: https://github.com/databooth/mojo-fireplace

## New Repository Structure

```
mojo-marimo/
├── .github/
│   └── workflows/
│       └── ci.yml.OFF          # Placeholder CI workflow (disabled)
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE                      # Apache License 2.0
├── MIGRATION.md                 # This file
├── README.md                    # Main documentation
├── pyproject.toml              # uv/pip configuration
├── pixi.toml                   # pixi configuration
├── docs/
│   ├── README.md               # Detailed usage guide
│   ├── SUMMARY.md              # Implementation overview
│   └── blog_post_draft.md      # Blog post for databooth.com.au
├── notebooks/
│   ├── example_notebook.py     # Interactive demo
│   └── benchmark_notebook.py   # Performance comparison
├── src/
│   └── mojo_marimo/
│       ├── __init__.py         # Package initialization
│       ├── compute.mojo        # Standalone Mojo implementations
│       ├── compute_wrapper.py  # Approach 1: Uncached subprocess
│       ├── mo_run_cached.py    # Approach 2: Cached binary
│       ├── mojo_decorator.py   # Approach 3: Decorator
│       └── test_all_approaches.py  # Setup verification
├── tests/
│   └── test_imports.py         # Basic import tests
└── examples/                    # Reserved for future examples
```

## Key Changes from Original

### Directory Structure

- **src/marimo_mojo/** → **src/mojo_marimo/**
  - Changed to match package naming convention (underscores instead of hyphens)
  - Now a proper Python package with `__init__.py`

- **Notebooks moved**: From `src/marimo_mojo/` to dedicated `notebooks/` directory
  - `example_notebook.py`
  - `benchmark_notebook.py`

- **Documentation moved**: From `src/marimo_mojo/*.md` to `docs/`
  - `README.md`
  - `SUMMARY.md`
  - `blog_post_draft.md`

### New Files Added

1. **pyproject.toml** - For uv/pip users (default installation method)
2. **pixi.toml** - Alternative installation for pixi users
3. **CONTRIBUTING.md** - Contribution guidelines
4. **CHANGELOG.md** - Version history
5. **LICENSE** - Apache License 2.0
6. **.gitignore** - Comprehensive ignore rules
7. **.github/workflows/ci.yml.OFF** - Placeholder CI workflow
8. **tests/test_imports.py** - Basic package tests
9. **src/mojo_marimo/__init__.py** - Package initialization and exports

### Environment Management

The new repo supports **two installation methods**:

1. **uv (Recommended)** - Default, modern Python package management
   ```bash
   uv venv
   uv pip install -e ".[dev]"
   ```

2. **pixi** - Alternative for conda users
   ```bash
   pixi install
   pixi run test-setup
   ```

This dual approach accommodates different user preferences and workflows.

### Package Structure

The code is now a proper Python package:

```python
from mojo_marimo import mojo  # Decorator
from mojo_marimo import fibonacci, sum_squares, is_prime  # Uncached
from mojo_marimo import fibonacci_cached, clear_cache  # Cached
```

### Version

- **Initial version**: v0.1.0
- Follows semantic versioning
- Ready for PyPI distribution (future)

## Files Not Migrated

The following were intentionally left in `mojo-fireplace`:

- Other example projects (advent_of_code, black_scholes, game_of_life, etc.)
- mojo-fireplace specific pixi configuration
- mojo-fireplace tests unrelated to marimo integration

## Next Steps

1. **Create GitHub repository**: https://github.com/databooth/mojo-marimo
2. **Push initial commit**:
   ```bash
   git remote add origin git@github.com:databooth/mojo-marimo.git
   git branch -M main
   git push -u origin main
   ```
3. **Add repository description**: "Interactive Mojo integration for Python notebooks"
4. **Add topics**: mojo, marimo, notebooks, performance, python
5. **Enable GitHub Pages** (optional, for docs)
6. **Publish blog post** to databooth.com.au
7. **Consider PyPI release** (optional, for v0.2.0+)

## Testing the New Repo

### Using uv

```bash
cd /Users/mjboothaus/code/github/databooth/mojo-marimo

# Install
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Verify
python src/mojo_marimo/test_all_approaches.py

# Run notebook
marimo edit notebooks/example_notebook.py
```

### Using pixi

```bash
cd /Users/mjboothaus/code/github/databooth/mojo-marimo

# Install
pixi install

# Verify
pixi run test-setup

# Run notebook
pixi run notebook-example
```

## Related Repositories

- [mojo-fireplace](https://github.com/databooth/mojo-fireplace) - Original source, contains other Mojo examples
- [mojo-dotenv](https://github.com/databooth/mojo-dotenv) - `.env` file parser for Mojo
- [mojo-toml](https://github.com/databooth/mojo-toml) - TOML parser for Mojo

## Notes

- The original code remains in `mojo-fireplace` for now (consider removing after confirming new repo works)
- This is a **standalone** project, not a submodule
- Blog post draft is included in `docs/` for reference when publishing
- CI workflow is disabled (`.OFF` extension) until ready for automated testing
