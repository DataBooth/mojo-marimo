# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-19

### Added

#### Core Functionality
- **Three integration patterns** for running Mojo from Python:
  - Decorator pattern (`@mojo`) - clean, Pythonic syntax with template parameters
  - Executor pattern (`run_mojo()`) - dynamic code execution from strings or files
  - Extension module pattern - compiled `.so` files for zero-overhead FFI calls
- **SHA256-based binary caching** in `~/.mojo_cache/binaries/`
- **Pre-compilation validation** catching common Mojo syntax errors:
  - Missing `fn main()`
  - File-scope statements outside functions
  - Missing colons in function definitions
  - Mixed tabs/spaces indentation
  - Deprecated `let` keyword → `var`
  - Python-style `int`/`str`/`bool` → Mojo `Int`/`String`/`Bool`
  - Print statements without parentheses
  - Missing parentheses in function calls
- **Cache management utilities**: `clear_cache()`, `cache_stats()`
- **Mojo version detection**: `get_mojo_version()`

#### Examples & Notebooks
- **Pattern demonstration notebooks** (marimo format):
  - `pattern_decorator.py` - decorator pattern with validation examples
  - `pattern_executor.py` - executor pattern with syntax error handling
  - `pattern_extension.py` - extension module pattern
- **Interactive example notebooks**:
  - Monte Carlo π estimation (3 patterns: decorator, executor, extension)
  - Mandelbrot set visualization (3 patterns: decorator, executor, extension)
  - Interactive learning notebook with sliders and visualisation
- **Jupyter notebook exports** in `notebooks/jupyter/` (`.ipynb` format)
- **Standalone Mojo files** for reference:
  - `examples/monte_carlo.mojo` and `examples/monte_carlo_ext.mojo`
  - `examples/mandelbrot.mojo` and `examples/mandelbrot_ext.mojo`

#### Testing & Quality
- **44 passing tests** with 75% code coverage
- **pytest** with coverage reporting
- **Ruff** for linting and formatting
- **ty** for type checking
- Test coverage for all three patterns, validation, and caching

#### Documentation
- Comprehensive README with quickstart and API docs
- Forum announcements for Modular and marimo communities
- `docs/FEEDBACK_REQUESTED.md` for community input
- `docs/ROADMAP.md` outlining future direction
- Pattern comparison and use case documentation

#### Development Tools
- **justfile** with 20+ commands for common tasks
- **pixi** and **uv** support for environment management
- Automated setup verification script (`scripts/verify_setup.py`)
- Pre-commit hooks configuration
- `check-mojo-build` recipe to validate all `.mojo` files compile

#### Dependencies
- `marimo` - interactive notebook framework
- `mojo` - Mojo compiler and runtime (auto-installed)
- `plotly` - visualisation in examples
- `numpy` - data handling in examples

### Changed
- Package description clarifies **notebook-agnostic** nature (works with Jupyter, VSCode, IPython, not just marimo)
- Updated all Mojo code to use `var` instead of deprecated `let` keyword
- Improved error messages with actionable hints

### Fixed
- Colon validation now correctly catches missing colons in function signatures with return types
- Executor notebooks properly handle string return values (not object attributes)
- Extension module notebooks updated to match current Mojo FFI patterns

### Known Limitations
- Subprocess overhead (~10-50ms) for decorator/executor patterns
- Extension modules require manual `PythonModuleBuilder` boilerplate
- macOS (Apple Silicon) tested; Linux/Windows support untested
- Single Mojo version support (0.25.7)
- Package name (`mojo-marimo`) doesn't reflect notebook-agnostic nature

---

## [Unreleased]

See [ROADMAP.md](docs/ROADMAP.md) for planned features.

[0.1.0]: https://github.com/databooth/mojo-marimo/releases/tag/v0.1.0
