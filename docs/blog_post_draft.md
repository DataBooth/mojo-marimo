---
title: "Interactive Mojo 🔥: Running High-Performance Code in Notebooks"
date: 2026-01-18
tags: Mojo 🔥, Python, Notebooks, Performance, Interactive Computing, marimo
status: Work in Progress
description: "Three practical approaches for running high-performance Mojo code from Python notebooks—decorators, executors, and extension modules—with real benchmarks and community feedback requested."
---

# Interactive Mojo 🔥: Running High-Performance Code in Notebooks

> **Status**: Work in progress — Released for community feedback and testing (v0.1.0 Beta)

## Why: The Interactive Performance Gap

Python notebooks are brilliant for exploration, visualisation, and rapid prototyping (if fact some stretch them well beyond this e.g. `nbdev`). But when you need serious performance, whether it's Monte Carlo simulations, numerical algorithms, or data transformations—Python sometimes hits a wall. Traditional solutions mean:

- **Rewriting in C/C++**: Complex build systems, manual memory management, days of work
- **Numba/JAX**: Limited language features, steep learning curves, debugging challenges
- **Pure Python optimisation**: Rarely gets you the 10-100× speedup you actually need

**The question**: What if you could write high-performance Mojo code and run it interactively from Python notebooks with minimal friction?

This matters for:
- **Data scientists** exploring algorithms that need real performance, not just toy datasets
- **Quant developers** prototyping trading strategies or risk models that need sub-millisecond execution
- **ML engineers** benchmarking preprocessing pipelines or custom operators
- **Educators** teaching performance engineering with immediate visual feedback

The ideal would be: _write Mojo once, call it like Python, see results instantly in an interactive notebook._

## What: Three Practical Approaches

I've been building `mojo-marimo`, exploring how to run Mojo code from [marimo](https://marimo.io/) notebooks (reactive Python notebooks). After experimenting with several patterns, **three approaches** emerged with distinct trade-offs:

1. **Decorator** — Clean API, notebook-friendly, subprocess overhead
2. **Executor** — Dynamic code generation, subprocess overhead
3. **Extension modules** — Zero overhead, more complex Mojo code

All solve the same problem—executing Mojo from Python—but optimise for different priorities.

### Approach 1: Executor (Dynamic Code)

**Pattern**: Pass Mojo code as string → Compile to binary → Cache by SHA256 hash → Execute

```python
from mojo_marimo import run_mojo

# Inline Mojo code
mojo_code = """
fn compute(n: Int) -> Int:
    return n * n

fn main():
    print(compute(42))
"""

# First call: ~1-2s (compile + run)
result = run_mojo(mojo_code)

# Subsequent calls: ~10-50ms (cached binary)
result = run_mojo(mojo_code)

# Or execute .mojo files
result = run_mojo("path/to/module.mojo")
```

**When to use**:
- Dynamic code generation (building Mojo from templates)
- Prototyping different algorithm variations
- Running existing .mojo files from Python

**Performance**: First call ~1-2s, subsequent calls ~10-50ms

**Trade-offs**: Flexible, explicit, subprocess overhead (~10-50ms per call).

### Approach 2: Decorator (Pythonic API)

**Pattern**: Extract Mojo from docstring → Use cached binary execution → Clean Python interface

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
    ...

# Use like normal Python!
result = fibonacci(10)
```

**When to use**:
- Clean APIs in notebook cells
- Self-documenting code (Mojo implementation visible in docstring)
- When you want performance without sacrificing Pythonic style

**Performance**: First call ~1-2s, subsequent calls ~10-50ms

**Trade-offs**: Most Pythonic, self-documenting, subprocess overhead (~10-50ms per call).

### Approach 3: Extension Modules (Zero Overhead)

**Pattern**: Compile Mojo to `.so` file → Direct Python import → No subprocess

```python
import mojo.importer  # Auto-compile on import
import fibonacci_mojo_ext

# Direct function call - zero subprocess overhead!
result = fibonacci_mojo_ext.fibonacci(100)
result = fibonacci_mojo_ext.is_prime(17)
```

**Mojo code** (requires `PythonModuleBuilder`):
```mojo
from python.python import PythonModuleBuilder

fn fibonacci(py_n: PythonObject) raises -> PythonObject:
    let n = Int(py_n)
    if n <= 1:
        return n
    # ... implementation
    return result

fn initialize(module: PythonModuleBuilder) -> None:
    module.add_function("fibonacci", fibonacci)
```

**When to use**:
- Performance-critical paths called 1000s of times
- Production systems where ~10-50ms overhead matters
- When you need C/Rust-level call overhead

**Performance**: First import ~1-2s (compile), subsequent calls ~0.01-0.1ms

**Trade-offs**: **1000× faster** than subprocess approaches, but requires more complex Mojo code and `PythonModuleBuilder` knowledge.

## How: Real Implementation Details

### The Cache Strategy

The cached approaches use SHA256 hashing of source code to uniquely identify implementations:

```python
# Cache location: ~/.mojo_cache/binaries/
# Key: SHA256(mojo_source)[:16]
# Example: ~/.mojo_cache/binaries/a3f9c2e8d1b4f7a2
```

Benefits:
- Cache persists across sessions
- Different implementations don't collide
- No manual cache invalidation needed
- Simple to clear: `clear_cache()`

### Benchmark Results (Preliminary)

Testing on Apple Silicon (M-series) with `fibonacci(10)`, `sum_squares(100)`, and `is_prime(104729)`:

| Approach | First Call | Subsequent Calls | Overhead | Use Case |
|----------|-----------|------------------|----------|----------|
| Executor | ~1-2s | ~10-50ms | Subprocess | Dynamic code, prototyping |
| Decorator | ~1-2s | ~10-50ms | Subprocess | Clean APIs, notebook-friendly |
| Extension | ~1-2s | ~0.01-0.1ms | None | Performance-critical loops |

Key insights:
1. **Decorator and executor have identical performance**: Both use subprocess + caching
2. **Extension modules eliminate overhead**: ~1000× faster per call, but more complex
3. **Choose based on bottleneck**: ~10-50ms okay? Use decorator. Need faster? Use extensions.
4. **First call is acceptable**: 1-2s compilation is fine for interactive work
5. **Real Mojo performance**: No Python fallbacks or compromises

### The marimo Advantage

Why [marimo](https://marimo.io/) specifically?

- **Reactive execution**: Change a slider, Mojo re-runs automatically
- **Pure Python files**: Version control friendly (unlike Jupyter JSON)
- **Type-safe**: Built-in UI elements with proper types
- **Reproducible**: Dependency graph prevents hidden state bugs

Example marimo cell using the decorator approach:

```python
import marimo as mo
from mojo_decorator import fibonacci

# Reactive slider
fib_n = mo.ui.slider(1, 30, value=10, label="n")

# Mojo executes automatically when slider changes
result = fibonacci(fib_n.value)

# Display with markdown
mo.md(f"**Fibonacci({fib_n.value})** = {result}")
```

This creates an interactive widget where dragging the slider triggers real Mojo execution and updates the result instantly.

### Extension Module Auto-Compilation

The extension module approach uses `mojo.importer` for automatic compilation:

```python
import mojo.importer  # Registers import hook
import fibonacci_mojo_ext  # Auto-compiles on first import
```

**What happens**:
1. First import: Compiles `.mojo` → `.so` in `__mojocache__/` (~1-2s)
2. Subsequent imports: Uses cached `.so` (instant)
3. Source changes: Recompiles automatically (hash-based detection)

**Trade-off**: Best for production code or tight loops. Overkill if ~10-50ms is acceptable.

## Why This Matters for Business

For DataBooth clients and medium-sized businesses exploring high-performance computing:

**1. Rapid prototyping meets production speed**
   - Explore in notebooks, deploy to production without rewrites
   - No "prototype in Python, rewrite in C++" tax

**2. Transparent performance path**
   - Start with either approach (both work well)
   - Choose decorator for cleaner APIs
   - No architectural rewrites needed

**3. Educational value**
   - Teams can learn Mojo incrementally
   - Side-by-side Python/Mojo comparisons in one notebook
   - Real benchmarks with interactive visualisation

**4. Risk reduction**
   - No vendor lock-in (Mojo is open source)
   - Falls back gracefully (subprocess always works)
   - Clear performance visibility (cache hits/misses visible)

## Current Status & Feedback Requested

**This is a work-in-progress** (v0.1.0 Beta) released for community feedback.

The `mojo-marimo` repo now includes:
- ✅ **Three integration patterns** with interactive notebooks
- ✅ **44 passing tests** (75% coverage)
- ✅ **Python vs Mojo benchmarking** infrastructure
- ✅ **Extension module examples** with auto-compilation
- ✅ **Validation and error handling** with helpful hints
- ✅ **Reference .mojo files** for learning
- ✅ **Comprehensive documentation**

### I'm Particularly Interested In:

**Pattern Preferences**:
- Which pattern do you prefer and why?
- Is the decorator syntax intuitive?
- Does extension module complexity justify the performance gain?

**Use Cases**:
- What real-world problems would you solve with this?
- Where does ~10-50ms overhead become a bottleneck?
- Algorithm prototyping? Production notebooks? Education?

**Performance & Ergonomics**:
- Is the `{{param}}` template syntax clear?
- Should we auto-generate extension module boilerplate?
- What benchmarks would be valuable?

**marimo Integration**:
- How well does this fit marimo's reactivity model?
- Missing features for notebook workflows?
- Other compiled languages you'd want integration for?

**All feedback welcome** — issues, PRs, or comments below! This library evolves based on real-world usage.

## Try It Yourself

```bash
# Clone the repo
git clone https://github.com/databooth/mojo-marimo
cd mojo-marimo

# Install dependencies (requires mojo on PATH)
# Using uv (recommended)
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Or using pixi
pixi install

# Run tests
just test  # or: pytest

# Launch interactive notebooks
just notebook-decorator   # Decorator examples
just notebook-executor    # Executor examples  
just notebook-extension   # Extension module examples

# Benchmarking
just notebook-benchmark   # Python vs Mojo comparison
just benchmark-exec       # Pattern performance comparison
```

Full code, examples, and documentation at: [github.com/databooth/mojo-marimo](https://github.com/databooth/mojo-marimo)

## Reflections

Three weeks into deep Mojo exploration, and this is what excites me: **performance without the usual friction.**

The three-pattern approach gives you choices:
- **Start simple**: Decorator for notebook-friendly code
- **Go dynamic**: Executor for code generation
- **Optimise later**: Extension modules when you need them

It's not perfect—subprocess overhead is real (~10-50ms), compilation adds latency (~1-2s)—but for interactive exploration, it's the right trade-off. And when you need zero overhead, extension modules are there.

For businesses considering Mojo: this is how you start. Pick a performance bottleneck, port it to Mojo, wrap it with a decorator, benchmark it in a notebook. If you see 10-100× speedup (and you likely will), you've validated the path forward without betting the farm.

**Questions? Feedback? Your own Mojo integration patterns?** This is a work-in-progress and I'd genuinely love to hear from you. Comments are enabled below, or reach out via the [contact page](https://www.databooth.com.au/about/).

---

**About the Series**: This post is part of an ongoing exploration of Mojo for real-world data and AI workflows. See the full series at [databooth.com.au/posts/mojo](https://www.databooth.com.au/posts/mojo).

**About DataBooth**: I help medium-sized businesses leverage high-performance computing for data analytics and AI. Now offering Mojo-powered services that deliver 10-100× faster solutions without vendor lock-in. [Learn more](https://www.databooth.com.au/).
