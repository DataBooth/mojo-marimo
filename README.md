# py-run-mojo 🔥

**Notebook-agnostic Mojo integration for Python** - three patterns for running high-performance Mojo code from any Python environment.

> **Status:** ✅ **Beta** - Three working approaches, evolving based on real-world usage
>
> **Note:** This library works with **any Python notebook system** (Jupyter, marimo, VSCode, Google Colab) and even standalone Python scripts. It was previously called `mojo-marimo`; the new name reflects its notebook-agnostic scope—see [ROADMAP.md](docs/ROADMAP.md).

## Overview

`py-run-mojo` (formerly `mojo-marimo`) provides three distinct patterns for executing Mojo code from Python, each with different trade-offs:

1. **Decorator** (`@mojo`) - Clean Pythonic syntax with template parameters and caching
2. **Executor** (`run_mojo()`) - Dynamic execution from strings or files, great for code generation
3. **Extension Module** - Compiled `.so` files for zero-overhead FFI calls (~1000× faster than subprocess)

**Works everywhere:** Jupyter notebooks, marimo, VSCode notebooks, Google Colab, IPython REPL, or standalone Python scripts. The core library has no notebook-specific dependencies.

```python
from py_run_mojo import mojo

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

- [x] Three integration patterns (decorator, executor, extension modules)
- [x] Works with any Python environment (Jupyter, marimo, VSCode, IPython, scripts)
- [x] Interactive example notebooks in marimo and Jupyter (`.ipynb`) formats
- [x] SHA256-based binary caching (`~/.mojo_cache/binaries/`)
- [x] Pre-compilation validation (catches common syntax errors)
- [x] Cache management utilities (`clear_cache()`, `cache_stats()`)
- [x] Monte Carlo and Mandelbrot examples with visualisation
- [x] 44 passing tests (75% coverage)
- [x] Comprehensive documentation + roadmap

### Planned

See [ROADMAP.md](docs/ROADMAP.md) for full details:

- [ ] Validate Jupyter compatibility with real-world testing
- [ ] Auto-generate extension module boilerplate
- [ ] Pattern library for common algorithms
- [ ] Enhanced error handling and debugging
- [ ] Multiple Mojo version support
- [ ] Potential package rename (community feedback requested)

## Installation

`py-run-mojo` supports both `uv` (recommended) and `pixi` for environment management.

### Prerequisites

**None!** Mojo is now installed automatically as a Python package dependency.

### Option 1: uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/databooth/py-run-mojo
cd py-run-mojo

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
git clone https://github.com/databooth/py-run-mojo
cd py-run-mojo

# Install with pixi
pixi install

# Verify setup
pixi run test-setup

# Launch example notebook
pixi run notebook-example
```

## Quick Start

### Pattern 1: Decorator (Recommended)

```python
from py_run_mojo import mojo

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

# Use like normal Python!
result = sum_squares(10)  # First call: ~1-2s, subsequent: ~10-50ms
print(result)  # 385
```

### Pattern 2: Executor

```python
from py_run_mojo import run_mojo

mojo_code = """
fn compute(n: Int) -> Int:
    return n * n

fn main():
    print(compute(42))
"""

result = run_mojo(mojo_code)  # Or run_mojo("path/to/file.mojo")
print(result)  # "1764"
```

### Pattern 3: Extension Module

```python
import mojo.importer  # Enables auto-compilation of .mojo → .so
import monte_carlo_mojo_ext

# Direct FFI call - no subprocess overhead!
x, y, inside, pi_est, error = monte_carlo_mojo_ext.generate_samples(1_000_000)
print(f"π ≈ {pi_est:.6f} ± {error:.6f}")
```

See [`examples/`](examples/) and [`notebooks/`](notebooks/) for complete working examples.

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
uv run python -m py_run_mojo.decorator

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
- [**Compiled Languages Integration**](docs/COMPILED_LANGUAGES.md) - How compiled languages work with marimo

## Project Structure

```
py-run-mojo/
├── src/
│   └── py_run_mojo/          # Core library
│       ├── executor.py       # Cached Mojo execution
│       ├── decorator.py      # @mojo decorator
│       ├── validator.py      # Pre-compilation validation
│       └── __init__.py       # Package exports
├── examples/                 # Example implementations
│   ├── examples.py          # Python wrappers (fibonacci, etc.)
│   ├── examples.mojo        # Standalone Mojo code
│   └── reference/           # Reference .mojo files
├── benchmarks/              # Performance benchmarking
│   ├── python_baseline.py   # Pure Python implementations
│   ├── mojo_implementations.py  # Mojo implementations
│   ├── python_vs_mojo.py    # Python vs Mojo comparison notebook
│   └── execution_approaches.py  # Execution patterns comparison
├── notebooks/               # Interactive marimo notebooks
│   ├── pattern_decorator.py # @mojo decorator examples
│   ├── pattern_executor.py  # run_mojo() examples
│   ├── interactive_learning.py  # Learning notebook
│   └── gpu_puzzles/         # marimo notebooks scaffolding Mojo GPU Puzzles
├── scripts/                 # Utility scripts
│   └── verify_setup.py      # Setup verification
├── tests/                   # Test suite
├── docs/                    # Documentation
│   ├── project/            # Project docs (contributing, changelog)
│   ├── blog_post_draft.md  # Blog post
│   ├── COMPILED_LANGUAGES.md  # Compiled language integration
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
