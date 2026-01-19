# mojo-marimo: High-Performance Mojo Execution in marimo Notebooks 🔥

Hi marimo community! I built **mojo-marimo** to bring high-performance [Mojo](https://www.modular.com/mojo) code execution to marimo notebooks.

## What is Mojo?

Mojo is a new systems programming language from Modular that combines Python's ease-of-use with C-level performance. It's designed for AI/ML infrastructure and can be 10-100× faster than Python for numerical computing.

## What does mojo-marimo do?

It lets you write and execute Mojo code directly in your marimo notebooks with two elegant patterns:

### Pattern 1: @mojo Decorator
```python
import marimo as mo
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
    ...

# Reactive slider
n_slider = mo.ui.slider(1, 30, value=10)

# Mojo executes on every slider change!
result = fibonacci(n_slider.value)

mo.md(f"{n_slider}\n\n**Fibonacci({n_slider.value})** = {result}")
```

### Pattern 2: run_mojo() for Dynamic Code
```python
from mojo_marimo import run_mojo

# Generate Mojo code dynamically
operation = mo.ui.dropdown(["add", "multiply", "power"])

mojo_code = f"""
fn compute(a: Int, b: Int) -> Int:
    return a {operation.value} b

fn main():
    print(compute(5, 3))
"""

result = run_mojo(mojo_code)
```

## Perfect for marimo's Reactivity

marimo's reactive execution model is **perfect** for this use case:

✅ **Instant feedback** - Change a slider, Mojo recompiles (if needed) and runs  
✅ **Smart caching** - Same code → reuse cached binary (~10-50ms)  
✅ **Visual exploration** - Build interactive demos with real performance  
✅ **Pure Python files** - Everything is `.py`, git-friendly  

## Use Cases

**Algorithm Prototyping:**
```python
# Try different algorithms interactively
algorithm = mo.ui.dropdown(["bubble_sort", "quick_sort", "merge_sort"])
data_size = mo.ui.slider(100, 10000, value=1000)

# Generate Mojo code for selected algorithm
mojo_code = generate_sorting_code(algorithm.value, data_size.value)
benchmark_result = run_mojo(mojo_code)
```

**Performance Exploration:**
```python
# Compare Python vs Mojo side-by-side
n = mo.ui.slider(1, 1000000, value=10000)

python_time = benchmark_python(n.value)
mojo_time = benchmark_mojo(n.value)

speedup = python_time / mojo_time
mo.md(f"**Speedup: {speedup:.1f}×**")
```

**Educational Demos:**
- Show how Mojo handles SIMD operations
- Visualize performance characteristics
- Interactive compiler behaviour exploration

## Features

✅ **Real Mojo Performance** - Actual compilation and execution  
✅ **Cached Binaries** - SHA256-based caching in `~/.mojo_cache/`  
✅ **Type Safe** - Automatic Python ↔ Mojo type conversion  
✅ **Two Patterns** - Decorator for clean APIs, executor for flexibility  
✅ **Pure Python** - All marimo notebooks are `.py` files  

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
# Clean decorator examples (fibonacci, primes, gcd)
marimo edit notebooks/decorator_notebook.py

# Dynamic code generation examples
marimo edit notebooks/executor_notebook.py

# Performance benchmarks
marimo edit notebooks/benchmark_notebook.py
```

## Technical Implementation

The library compiles Mojo code to binaries on first execution and caches them by content hash. Subsequent calls with the same code reuse the cached binary, making it blazing fast (~10-50ms vs ~1-2s for compilation).

The `@mojo` decorator extracts Mojo code from function docstrings and handles parameter substitution using `{{param}}` syntax, similar to template engines.

## Performance

Typical performance on Apple Silicon:

| Call Type | Time | What Happens |
|-----------|------|--------------|
| First call | ~1-2s | Compile Mojo + execute |
| Subsequent | ~10-50ms | Execute cached binary |
| Python equivalent | Variable | Usually much slower |

Real speedups depend on the algorithm, but 10-100× faster than pure Python is common for numerical code.

## Repository

🔗 https://github.com/DataBooth/mojo-marimo

- 27 passing tests
- Complete documentation
- Interactive example notebooks
- Benchmark comparisons
- Supports both uv and pixi

## What I Love About This Combination

marimo's reactive model + Mojo's performance = **Interactive High-Performance Computing**

It's like Jupyter for serious numerical work, but with marimo's superior notebook UX (pure Python files, true reactivity, no hidden state).

## Questions?

Happy to answer questions or hear feedback! I'm particularly interested in:
- What numerical/performance-critical tasks would you explore with this?
- Other languages you'd want similar integration for?
- Feature requests?

Try it out and let me know what you think! 🚀

---

**Tech Stack:** Mojo 0.25.7, marimo 0.19.4, Python 3.12-3.14  
**License:** Apache-2.0  
**Tested on:** macOS (Apple Silicon + Intel), Linux planned
