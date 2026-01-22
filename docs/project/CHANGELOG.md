# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-01-22

### Changed
- Renamed project from `mojo-marimo` to `py-run-mojo` to emphasise notebook-agnostic usage.
- Updated Python package name to `py_run_mojo` and refreshed examples/docs accordingly.

## [0.1.0] - 2026-01-18

### Added
- Three integration approaches for running Mojo from Python/marimo notebooks:
  - Uncached subprocess (simple, transparent)
  - Cached binary (performance-optimised for repeated execution)
  - Decorator pattern (clean Pythonic syntax)
- SHA256-based binary caching system (`~/.mojo_cache/binaries/`)
- Cache management utilities (`clear_cache()`, `cache_stats()`)
- Interactive marimo notebooks:
  - `example_notebook.py` - Reactive UI demo with sliders
  - `benchmark_notebook.py` - Comprehensive performance comparison
- Setup verification script (`test_all_approaches.py`)
- Support for both `uv` (recommended) and `pixi` environment management
- Comprehensive documentation:
  - Main README with installation and usage guide
  - Detailed implementation docs (SUMMARY.md)
  - Blog post draft for databooth.com.au
- Example Mojo implementations:
  - `fibonacci()` - Iterative Fibonacci calculation
  - `sum_squares()` - Sum of squares computation
  - `is_prime()` - Primality testing

### Documentation
- Installation guide for both uv and pixi users
- Quick start examples for all three approaches
- Performance comparison table with benchmarks
- API reference for all functions
- Project structure overview
- Contributing guidelines

[0.1.2]: https://github.com/databooth/mojo-marimo/releases/tag/v0.1.2
[0.1.0]: https://github.com/databooth/mojo-marimo/releases/tag/v0.1.0
