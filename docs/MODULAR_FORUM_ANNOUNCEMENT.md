# Announcing mojo-marimo: Run Mojo in Interactive Python Notebooks 🔥

> **Status**: Work in progress - Released for community feedback and testing  
> **Version**: v0.1.0 (Beta)

I'm excited to share **mojo-marimo** - a library that lets you run real Mojo code inside interactive Python notebooks using marimo.

**Note:** This executes Mojo via compilation and subprocess/FFI, **not** as a Mojo kernel.

This is an early release and **I'm actively seeking feedback** from the Mojo community on the approach, API design, and use cases.

## What is it?

`mojo-marimo` provides **three integration patterns** for executing high-performance Mojo code from Python/marimo notebooks:

### Pattern 1: Decorator - Pythonic & Clean
Mojo code lives in function docstrings with `{{param}}` templates. Call it like normal Python.

**Example:** [`notebooks/pattern_decorator.py`](https://github.com/DataBooth/mojo-marimo/blob/main/notebooks/pattern_decorator.py)

### Pattern 2: Executor - Dynamic & Flexible  
Pass Mojo code as strings or execute `.mojo` files. Perfect for dynamic code generation.

**Example:** [`notebooks/pattern_executor.py`](https://github.com/DataBooth/mojo-marimo/blob/main/notebooks/pattern_executor.py)

### Pattern 3: Extension Modules - Zero Overhead
Compile to `.so` files for direct Python imports. No subprocess, ~1000× faster calls.

**Examples:**
- [`notebooks/monte_carlo_extension.py`](https://github.com/DataBooth/mojo-marimo/blob/main/notebooks/monte_carlo_extension.py) - π estimation with scatter plots
- [`notebooks/mandelbrot_extension.py`](https://github.com/DataBooth/mojo-marimo/blob/main/notebooks/mandelbrot_extension.py) - Fractal visualisation

**Trade-off**: More complex Mojo code (requires [`PythonModuleBuilder`](https://docs.modular.com/mojo/stdlib/python/PythonModuleBuilder)), but eliminates subprocess overhead.

## Key Features

✅ Real Mojo compilation and execution  
✅ Smart caching (SHA256-based)  
✅ Three integration patterns  
✅ Pre-compilation validation  
✅ Interactive examples: Fibonacci, Monte Carlo π, Mandelbrot fractals  
✅ Works with marimo's reactive model

## Repository

🔗 https://github.com/DataBooth/mojo-marimo

44 passing tests (75% coverage) | Three integration patterns | Interactive examples | Comprehensive documentation

## 🎯 Feedback Requested!

See [`docs/FEEDBACK_REQUESTED.md`](https://github.com/DataBooth/mojo-marimo/blob/main/docs/FEEDBACK_REQUESTED.md) for specific areas where community input would be valuable.

---

**Tech Stack:** Mojo, Python, marimo, uv  
**License:** Apache-2.0  
**Tested on:** macOS (Apple Silicon), Python 3.12-3.14, Mojo 0.25.7

