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

**Critical**: The `mojo` command must be available on your PATH.

```bash
# Install Mojo
curl https://get.modular.com | sh -
modular install mojo

# Add to PATH (example for macOS/Linux)
export PATH="$HOME/.modular/pkg/packages.modular.com_mojo/bin:$PATH"

# Verify
mojo --version
```

### Option 1: uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/databooth/mojo-marimo
cd mojo-marimo

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Verify setup
python src/mojo_marimo/test_all_approaches.py

# Launch example notebook
marimo edit notebooks/example_notebook.py
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
# Using uv
uv run python scripts/verify_setup.py

# Using pixi
pixi run test-setup
```

This checks that `mojo` is available and tests all three approaches.

### Interactive Notebooks

```bash
# Example notebook (uv)
marimo edit notebooks/example_notebook.py

# Example notebook (pixi)
pixi run notebook-example

# Benchmark comparison (uv)
marimo edit notebooks/benchmark_notebook.py

# Benchmark comparison (pixi)
pixi run notebook-benchmark
```

### Command-Line Testing

```bash
# Using uv
python src/mojo_marimo/compute_wrapper.py       # Uncached
python src/mojo_marimo/mo_run_cached.py         # Cached
python src/mojo_marimo/mojo_decorator.py        # Decorator

# Using pixi
pixi run demo-uncached
pixi run demo-cached
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

- [**README.md**](docs/README.md) - Detailed usage guide
- [**SUMMARY.md**](docs/SUMMARY.md) - Implementation overview and design decisions
- [**blog_post_draft.md**](docs/blog_post_draft.md) - Long-form explanation and business context

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
│   ├── example_notebook.py  # Interactive demo
│   └── benchmark_notebook.py # Performance comparison
├── scripts/                 # Utility scripts
│   └── verify_setup.py      # Setup verification
├── tests/                   # Test suite
├── docs/                    # Documentation
└── README.md                # This file
```

## Development

### Using uv

```bash
# Install in development mode
uv pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
ruff format .

# Lint
ruff check .

# Type check
uvx ty check
```

### Using pixi

```bash
# Run tests
pixi run test-all

# Format code
pixi run format

# Lint
pixi run lint

# Type check
pixi run typecheck
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
