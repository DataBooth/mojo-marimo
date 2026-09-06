# mojo-marimo: High-Performance Mojo Execution in marimo Notebooks 🔥

> **Status**: Work in progress - Released for community feedback and testing  
> **Version**: v0.1.0 (Beta)

Hi marimo community! I built **mojo-marimo** to bring high-performance [Mojo](https://www.modular.com/mojo) code execution to marimo notebooks.

**This is an early release** - feedback on the approach and API design is very welcome!

## What is Mojo?

Mojo is a systems programming language from Modular that combines Python's ease-of-use with C-level performance, designed for AI/ML infrastructure.

## What does mojo-marimo do?

It lets you write and execute Mojo code directly in marimo notebooks with **three integration patterns**:

### 1. Decorator Pattern - Clean & Pythonic
Mojo code lives in docstrings with `{{param}}` template syntax:
```python
from py_run_mojo import mojo

@mojo
def fibonacci(n: int) -> int:
    """[Mojo code here with {{n}} placeholder]"""
    ...

result = fibonacci(10)  # Called like normal Python
```

### 2. Executor Pattern - Dynamic Code Generation  
Pass Mojo code as strings for runtime flexibility:
```python
from py_run_mojo import run_mojo

mojo_code = f"""[Generated Mojo code]"""
result = run_mojo(mojo_code)
```

### 3. Extension Modules - Zero Overhead
Compile to `.so` files for direct Python imports:
```python
import mojo.importer
import my_mojo_ext

result = my_mojo_ext.compute(100)  # Direct call, no subprocess
```
**Trade-off**: More complex Mojo code (requires `PythonModuleBuilder`)

See working examples in the [repository notebooks](https://github.com/DataBooth/mojo-marimo/tree/main/notebooks).

## Why marimo?

marimo's reactive execution model pairs perfectly with Mojo:
- ✅ **Reactive sliders/controls** trigger Mojo recompilation and execution  
- ✅ **Smart caching** - Same code reuses cached binaries
- ✅ **Pure Python files** - Everything is `.py`, git-friendly  
- ✅ **Visual feedback** - Interactive demos with real performance

## Use Cases

- Algorithm prototyping with interactive parameters
- Side-by-side Python vs Mojo performance comparisons  
- Educational demos (SIMD, compiler behaviour, optimization)
- Exploring Mandelbrot fractals, Monte Carlo simulations, numerical methods

## Features

✅ Real Mojo compilation and execution  
✅ Binary caching (SHA256-based)  
✅ Three integration patterns  
✅ Pre-compilation validation with helpful hints  
✅ Example notebooks: Fibonacci, Monte Carlo π, Mandelbrot fractals

## Getting Started

**Installation:**
```bash
# Requires Mojo: pip install mojo

git clone https://github.com/DataBooth/mojo-marimo
cd mojo-marimo

# Install with uv (recommended)
uv sync --extra dev

# Or with pixi
pixi install
```

**Try the notebooks:**
```bash
just notebook-decorator        # Decorator examples
just notebook-mc-extension     # Monte Carlo π estimation  
just notebook-mandelbrot-extension  # Mandelbrot fractals

# Or directly with marimo
marimo edit notebooks/pattern_decorator.py
marimo edit notebooks/monte_carlo_extension.py
```

## How It Works

Mojo code compiles to binaries on first execution and caches them (SHA256 hash). Subsequent calls reuse the cached binary. The `@mojo` decorator extracts Mojo from docstrings and handles `{{param}}` template substitution.

## Repository

🔗 https://github.com/DataBooth/mojo-marimo

- 44 passing tests (75% coverage)
- Interactive example notebooks (Fibonacci, Monte Carlo, Mandelbrot)
- Complete documentation
- Supports uv and pixi

## 🎯 Feedback Welcome!

This is an early release - I'd love your input on:

- **Pattern preferences**: Which approach works best for your workflows?  
- **Use cases**: What problems would you solve with this?
- **marimo integration**: How well does this fit the reactive model?
- **API ergonomics**: Is the `{{param}}` syntax intuitive?

**All feedback welcome** - issues, PRs, or comments! Try it out and let me know what you think! 🚀

---

**Tech Stack:** Mojo 0.25.7, marimo 0.19.4+, Python 3.12-3.14  
**License:** Apache-2.0  
**Tested on:** macOS (Apple Silicon), Python 3.12-3.14, Mojo 0.25.7
