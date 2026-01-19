# mojo-marimo 🔥

Interactive Mojo integration for Python notebooks - three patterns for running high-performance Mojo code from marimo notebooks.

> **Status:** ✅ **Beta** - Three working approaches, evolving based on real-world usage

## Overview

`mojo-marimo` provides three distinct patterns for executing Mojo code from Python/marimo notebooks, each with different trade-offs between speed, simplicity, and developer experience:

1. **Uncached Subprocess** - Simple, transparent, best for development (~50-200ms per call)
2. **Cached Binary** - Fast repeated execution (~10-50ms after first compile)
3. **Decorator** - Clean Pythonic syntax with cached performance

```python
from mojo_marimo import mojo

@mojo
def fibonacci(n: int) -> int:
    """
    fn fibonacci(n: Int) -> Int:
        if n <= 1:
            return n
        var prev: Int = 0
        var curr: Int = 1
        for _ in range(2, n + 1):
            var next_val = prev + curr
            prev = curr
            curr = next_val
        return curr
    
    fn main():
        print(fibonacci({{n}}))
    """
    pass

# Use like normal Python!
result = fibonacci(10)
```

## Why This Exists

Python notebooks are brilliant for exploration, but hit a wall when you need serious performance. Traditional solutions—rewriting in C/C++, using Numba/JAX, or pure Python optimisation—are either too complex or don't deliver the 10-100× speedup you need.

**The question**: What if you could write high-performance Mojo code and run it interactively from Python notebooks with minimal friction?

This matters for:
- **Data scientists** exploring algorithms that need real performance
- **Quant developers** prototyping trading strategies or risk models
- **ML engineers** benchmarking preprocessing pipelines or custom operators
- **Educators** teaching performance engineering with immediate visual feedback

## Features

### Current (v0.1.0)

- [x] Three integration approaches (uncached, cached, decorator)
- [x] Interactive marimo notebooks with reactive UI
- [x] Benchmark comparison notebook
- [x] SHA256-based binary caching (`~/.mojo_cache/binaries/`)
- [x] Cache management utilities (`clear_cache()`, `cache_stats()`)
- [x] Setup verification script
- [x] Comprehensive documentation

### Planned

- [ ] Jupyter notebook support
- [ ] VSCode notebook integration
- [ ] Python extension module approach (`.so` compilation)
- [ ] Pattern library for common use cases
- [ ] Enhanced error handling and debugging
- [ ] Multiple Mojo version support

## Installation

`mojo-marimo` supports both `uv` (recommended) and `pixi` for environment management.

### Prerequisites

**None!** Mojo is now installed automatically as a Python package dependency.

### Option 1: uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/databooth/mojo-marimo
cd mojo-marimo

# Install dependencies (includes mojo)
uv sync --extra dev

# Verify setup
uv run python scripts/verify_setup.py

# Launch example notebook
uv run marimo edit notebooks/example_notebook.py
```

### Option 2: pixi

```bash
# Clone the repository
git clone https://github.com/databooth/mojo-marimo
cd mojo-marimo

# Install with pixi
pixi install

# Verify setup
pixi run test-setup

# Launch example notebook
pixi run notebook-example
```

## Quick Start

### Using the Decorator (Recommended)

```python
import marimo as mo
from mojo_marimo import mojo

@mojo
def sum_squares(n: int) -> int:
    """
    fn sum_squares(n: Int) -> Int:
        var total: Int = 0
        for i in range(1, n + 1):
            total += i * i
        return total
    
    fn main():
        print(sum_squares({{n}}))
    """
    pass

# Reactive slider
n = mo.ui.slider(1, 100, value=10, label="n")

# Mojo executes automatically when slider changes
result = sum_squares(n.value)

mo.md(f"**Sum of squares 1² + 2² + ... + {n.value}²** = {result}")
```

### Using Cached Binary

```python
from mojo_marimo.mo_run_cached import sum_squares_cached

# First call: ~1-2s (compile + run)
result = sum_squares_cached(10)

# Subsequent calls: ~10-50ms (run only)
result = sum_squares_cached(20)
```

### Using Uncached Subprocess

```python
from mojo_marimo.compute_wrapper import sum_squares

# Every call compiles and runs
result = sum_squares(10)  # ~50-200ms
```

## Usage

### Verify Setup

```bash
# Using just
just test-setup

# Using uv
uv run python scripts/verify_setup.py

# Using pixi
pixi run test-setup
```

This checks that `mojo` is available and tests both approaches.

### Interactive Notebooks

```bash
# Using just
just notebook-decorator  # @mojo decorator examples
just notebook-executor   # run_mojo() examples
just benchmark          # Performance comparison

# Using uv
uv run marimo edit notebooks/pattern_decorator.py
uv run marimo edit notebooks/pattern_executor.py
uv run marimo edit notebooks/benchmark.py

# Using pixi
pixi run notebook-decorator
pixi run notebook-executor
pixi run benchmark
```

### Command-Line Demos

```bash
# Using just
just demo-examples
just demo-decorator

# Using uv
uv run python examples/examples.py
uv run python -m mojo_marimo.decorator

# Using pixi
pixi run demo-examples
pixi run demo-decorator
```

## Performance Comparison

Testing on Apple Silicon (M-series) with `fibonacci(10)`, `sum_squares(100)`, and `is_prime(104729)`:

| Approach | First Call | Subsequent Calls | Use Case |
|----------|-----------|------------------|----------|
| Uncached | ~50-200ms | ~50-200ms | Development, debugging |
| Cached | ~1-2s | ~10-50ms | Repeated execution |
| Decorator | ~1-2s | ~10-50ms | Production, clean code |

**Key insights**:
1. **Caching wins for repeated calls**: 5-10× faster after first compilation
2. **Decorator has zero performance cost**: Same speed as explicit caching, better developer experience
3. **All approaches deliver real Mojo performance**: No Python fallbacks or compromises

See the [benchmark notebook](notebooks/benchmark_notebook.py) for detailed comparisons.

## Documentation

### Project Documentation
- [**CONTRIBUTING.md**](docs/project/CONTRIBUTING.md) - Contribution guidelines
- [**CHANGELOG.md**](docs/project/CHANGELOG.md) - Version history
- [**Implementation Guide**](docs/project/README.md) - Detailed usage guide
- [**Technical Summary**](docs/project/SUMMARY.md) - Implementation overview

### Blog & Announcements
- [**Blog Post Draft**](docs/blog_post_draft.md) - Long-form explanation
- [**Modular Forum**](docs/MODULAR_FORUM_ANNOUNCEMENT.md) - Mojo community announcement
- [**marimo Community**](docs/MARIMO_ANNOUNCEMENT.md) - marimo community announcement

## Project Structure

```
mojo-marimo/
├── src/
│   └── mojo_marimo/          # Core library
│       ├── executor.py       # Cached Mojo execution
│       ├── decorator.py      # @mojo decorator
│       └── __init__.py       # Package exports
├── examples/                 # Example implementations
│   ├── examples.py          # Python wrappers (fibonacci, etc.)
│   └── examples.mojo        # Standalone Mojo code
├── notebooks/               # Interactive marimo notebooks
│   ├── pattern_decorator.py # @mojo decorator examples
│   ├── pattern_executor.py  # run_mojo() examples  
│   └── benchmark.py         # Performance comparison
├── scripts/                 # Utility scripts
│   └── verify_setup.py      # Setup verification
├── tests/                   # Test suite
├── docs/                    # Documentation
│   ├── project/            # Project docs (contributing, changelog)
│   ├── blog_post_draft.md  # Blog post
│   ├── MODULAR_FORUM_ANNOUNCEMENT.md
│   └── MARIMO_ANNOUNCEMENT.md
└── README.md                # This file
```

## Development

### Using just (Recommended)

We provide a `justfile` with common tasks synced across uv and pixi:

```bash
# Show all available commands
just --list

# Install dependencies
just install

# Run tests
just test
just test-coverage

# Code quality
just format
just lint
just typecheck
just check              # Run all quality checks

# Notebooks
just notebook-decorator
just notebook-executor
just benchmark

# Development
just clean
just clean-mojo-cache
just cache-stats

# CI checks locally
just ci
```

### Using uv

```bash
# Install in development mode
uv sync --extra dev

# Run tests
uv run pytest tests/

# Format code
uv run ruff format .

# Lint
uv run ruff check .

# Type check
uv run ty check
```

### Using pixi

```bash
# Run tests
pixi run test

# Format code
pixi run format

# Lint
pixi run lint

# Type check
pixi run typecheck

# All quality checks
pixi run check
```

## Why marimo?

[marimo](https://marimo.io/) is a reactive Python notebook with several advantages:

- **Reactive execution**: Change a slider, Mojo re-runs automatically
- **Pure Python files**: Version control friendly (unlike Jupyter JSON)
- **Type-safe**: Built-in UI elements with proper types
- **Reproducible**: Dependency graph prevents hidden state bugs

## Contributing

Contributions welcome! This is a living experiment, evolving based on real-world usage.

Areas for contribution:
- Additional notebook examples
- Performance profiling on diverse hardware
- Integration with other notebook environments
- Error handling improvements
- Documentation enhancements

## Related Projects

- [mojo-fireplace](https://github.com/databooth/mojo-fireplace) - Collection of Python-to-Mojo example projects
- [mojo-dotenv](https://github.com/databooth/mojo-dotenv) - Modern `.env` file parser for Mojo
- [mojo-toml](https://github.com/databooth/mojo-toml) - TOML parser for Mojo

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## About

Created by [Michael Booth](https://www.databooth.com.au/) at DataBooth.

Part of an ongoing exploration of Mojo for real-world data and AI workflows. See the full series at [databooth.com.au/posts/mojo](https://www.databooth.com.au/posts/mojo).

DataBooth helps medium-sized businesses leverage high-performance computing for data analytics and AI, now offering Mojo-powered services that deliver 10-100× faster solutions without vendor lock-in.
