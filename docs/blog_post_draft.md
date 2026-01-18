---
title: "Interactive Mojo 🔥: Three Patterns for Notebook Integration"
date: 2026-01-18
tags: Mojo 🔥, Python, Notebooks, Performance, Interactive Computing, marimo
description: "Exploring three approaches for running high-performance Mojo code from Python notebooks—uncached subprocess, cached binaries, and decorators—with real benchmarks and practical guidance."
---

# Interactive Mojo 🔥: Three Patterns for Notebook Integration

## Why: The Interactive Performance Gap

Python notebooks are brilliant for exploration, visualisation, and rapid prototyping. But when you need serious performance—whether it's Monte Carlo simulations, numerical algorithms, or data transformations—Python hits a wall. Traditional solutions mean:

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

## What: Three Integration Patterns

I've been building `mojo-fireplace` ([github.com/databooth/mojo-fireplace](https://github.com/databooth/mojo-fireplace))—a collection of paired Python and Mojo examples showing real-world migration paths. The latest addition explores running Mojo code from [marimo](https://marimo.io/) notebooks (reactive Python notebooks) through three distinct approaches.

Each approach tackles the same problem—executing Mojo from Python—but with different trade-offs between speed, simplicity, and developer experience.

### Approach 1: Uncached Subprocess

**Pattern**: Write temporary file → `mojo run` → Parse output → Cleanup

```python
from compute_wrapper import fibonacci

# Every call compiles and runs Mojo
result = fibonacci(10)  # ~50-200ms
```

**When to use**:
- Rapid prototyping where code changes frequently
- Debugging Mojo implementations
- Educational demos where seeing compilation is valuable

**Performance**: ~50-200ms per call (includes compilation every time)

**Trade-offs**: Simple and transparent, but slow for repeated calls. Best for development.

### Approach 2: Cached Binary

**Pattern**: First call compiles to binary → Cache by SHA256 hash → Reuse cached executable

```python
from mo_run_cached import fibonacci_cached

# First call: ~1-2s (compile + run)
result = fibonacci_cached(10)

# Subsequent calls: ~10-50ms (run only)
result = fibonacci_cached(10)
```

**When to use**:
- Benchmarking where you run the same code repeatedly
- Production notebooks with stable Mojo implementations
- Scenarios where a one-time compilation cost is acceptable

**Performance**: First call ~1-2s, subsequent calls ~10-50ms

**Trade-offs**: Much faster for repeated execution, cache persists across sessions, but requires explicit function wrapping.

### Approach 3: Decorator

**Pattern**: Extract Mojo from docstring → Use cached binary execution → Clean Python interface

```python
from mojo_decorator import mojo

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

**When to use**:
- Production code where ergonomics matter
- Self-documenting APIs (Mojo code is visible in the docstring)
- When you want performance without sacrificing Pythonic style

**Performance**: Same as cached binary (~10-50ms after first call)

**Trade-offs**: Most elegant, but requires decorator setup and understanding of template placeholders.

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

| Approach | First Call | Subsequent Calls | Use Case |
|----------|-----------|------------------|----------|
| Uncached | ~50-200ms | ~50-200ms | Development |
| Cached | ~1-2s | ~10-50ms | Repeated execution |
| Decorator | ~1-2s | ~10-50ms | Production code |

Key insights:
1. **Caching wins for repeated calls**: 5-10× faster than uncached after first compilation
2. **Decorator has zero performance cost**: Same speed as explicit caching, better DX
3. **All approaches deliver real Mojo performance**: No Python fallbacks or compromises

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

### What's Not Here (Yet)

A fourth approach—compiling Mojo to Python extension modules (`.so` files)—would eliminate subprocess overhead entirely:

- **Performance**: ~0.01-0.1ms per call (1000× faster than subprocess)
- **Complexity**: Requires PyInit wrapper generation, build toolchain
- **Trade-off**: Best for production with 1000s+ of calls, overkill for exploration

I'm keeping this in reserve. For interactive notebooks, the cached binary approach hits the sweet spot of simplicity and performance.

## Why This Matters for Business

For DataBooth clients and medium-sized businesses exploring high-performance computing:

**1. Rapid prototyping meets production speed**
   - Explore in notebooks, deploy to production without rewrites
   - No "prototype in Python, rewrite in C++" tax

**2. Transparent performance path**
   - Start with uncached for development
   - Graduate to cached/decorator for production
   - No architectural rewrites between phases

**3. Educational value**
   - Teams can learn Mojo incrementally
   - Side-by-side Python/Mojo comparisons in one notebook
   - Real benchmarks with interactive visualisation

**4. Risk reduction**
   - No vendor lock-in (Mojo is open source)
   - Falls back gracefully (subprocess always works)
   - Clear performance visibility (cache hits/misses visible)

## Current Status & Next Steps

The `mojo-fireplace` repo now includes:
- ✅ Three working integration approaches
- ✅ Interactive marimo notebooks with reactive UI
- ✅ Benchmark comparison notebook
- ✅ Setup verification script
- ✅ Comprehensive documentation

**Evolving areas**:
- Real-world performance profiling on diverse hardware
- Error handling and debugging workflow refinement
- Pattern library for common use cases (data transformations, simulations, etc.)
- Integration with popular notebook environments (Jupyter, VSCode)

This is a living experiment. The patterns work today, but I'm refining them based on real-world usage. If you're exploring Mojo for data-intensive work, these patterns provide a low-friction entry point.

## Try It Yourself

```bash
# Clone the repo
git clone https://github.com/databooth/mojo-fireplace
cd mojo-fireplace

# Install dependencies (requires mojo on PATH)
pixi install

# Verify setup
pixi run test-marimo-setup

# Launch interactive notebook
pixi run marimo-edit

# Or explore the benchmark comparison
pixi run benchmark-marimo
```

Full code, examples, and documentation at: [github.com/databooth/mojo-fireplace/src/marimo_mojo](https://github.com/databooth/mojo-fireplace/tree/main/src/marimo_mojo)

## Reflections

Three weeks into deep Mojo exploration, and this is what excites me: **performance without the usual friction.**

The decorator approach, in particular, feels like a genuine improvement over "write C extension" or "port to Numba". It's not perfect—subprocess overhead is real, compilation adds latency—but for interactive exploration, it's the right trade-off.

For businesses considering Mojo: this is how you start. Pick a performance bottleneck, port it to Mojo, wrap it with a decorator, benchmark it in a notebook. If you see 10-100× speedup (and you likely will), you've validated the path forward without betting the farm.

**Questions? Feedback? Your own Mojo integration patterns?** I'd genuinely love to hear from you. Comments are enabled below, or reach out via the [contact page](https://www.databooth.com.au/about/).

---

**About the Series**: This post is part of an ongoing exploration of Mojo for real-world data and AI workflows. See the full series at [databooth.com.au/posts/mojo](https://www.databooth.com.au/posts/mojo).

**About DataBooth**: I help medium-sized businesses leverage high-performance computing for data analytics and AI. Now offering Mojo-powered services that deliver 10-100× faster solutions without vendor lock-in. [Learn more](https://www.databooth.com.au/).
