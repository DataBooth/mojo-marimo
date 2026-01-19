# Marimo + Mojo Integration

## Why

Marimo is a reactive Python notebook that allows you to build interactive data apps. Integrating Mojo with marimo enables:
- Interactive exploration of high-performance Mojo code
- Real-time visualisation of Mojo computations
- Reactive UI components that leverage Mojo's speed
- Side-by-side comparison of Python vs Mojo implementations

**Use Cases:**
- Performance benchmarking dashboards
- Interactive algorithm visualisations
- Educational notebooks showing Python-to-Mojo transitions
- Data science workflows with Mojo-accelerated computations

## What

Examples demonstrating how to use Mojo within marimo notebooks through:
- Python interop to call Mojo functions
- Mojo extension modules exposed to Python
- Reactive visualisations of Mojo computations
- Performance comparison dashboards

**Files:**
- Coming soon: Example marimo notebooks with Mojo integration

## How

### Prerequisites

```bash
# Install marimo via pixi (already configured in pixi.toml)
pixi install

# Ensure Mojo is installed and available on PATH
curl https://get.modular.com | sh -
modular install mojo

# Add to PATH (example for macOS/Linux)
export PATH="$HOME/.modular/pkg/packages.modular.com_mojo/bin:$PATH"
```

**IMPORTANT**: The `mojo` command must be available on your PATH for all approaches to work.

### Three Approaches for Running Mojo from Python

This directory demonstrates three different patterns for executing Mojo code from Python/marimo notebooks:

#### 1. Uncached Subprocess (`compute_wrapper.py`)

**Pattern**: Write temp file → `mojo run` → Parse output (every call)

```python
from compute_wrapper import fibonacci

# Every call compiles and runs
result = fibonacci(10)
```

**When to use**:
- Rapid prototyping / development
- Code changes frequently
- Don't need optimal performance

**Performance**: ~50-200ms per call

#### 2. Cached Binary (`mo_run_cached.py`)

**Pattern**: First call compiles & caches, subsequent calls reuse binary

```python
from mo_run_cached import fibonacci_cached

# First call: ~1-2s (compile + run)
# Subsequent: ~10-50ms (run only)
result = fibonacci_cached(10)
```

**When to use**:
- Running same Mojo code repeatedly
- Need better performance than uncached
- Cache persists across sessions

**Performance**: First call ~1-2s, subsequent ~10-50ms

#### 3. Decorator (`mojo_decorator.py`)

**Pattern**: Decorator extracts Mojo from docstring, uses cached execution

```python
from mojo_decorator import fibonacci

# Clean Pythonic syntax, same performance as cached
result = fibonacci(10)
```

**When to use**:
- Want clean, Pythonic syntax
- Same performance as cached binary
- Prefer self-documenting code

**Performance**: Same as cached binary approach

### Running Examples

```bash
# Using pixi tasks (NOTE: mojo must be on PATH)
pixi run marimo-edit              # Interactive example notebook
pixi run benchmark-marimo         # Comparison & benchmark notebook
pixi run run-marimo-demo          # Test uncached approach
pixi run run-marimo-cached        # Test cached approach
pixi run run-marimo-decorator     # Test decorator approach

# Or directly with marimo (if installed)
cd src/marimo_mojo
marimo edit example_notebook.py
marimo edit benchmark_notebook.py
```

### Benchmark Results

See `benchmark_notebook.py` for comprehensive comparison showing:
- First-call latency (compilation time)
- Subsequent-call latency (execution time)
- Code usability comparison
- Performance recommendations

### Example: Using the Decorator

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

### Advantages

**All approaches**:
- ✅ Real Mojo execution (not Python fallbacks)
- ✅ Easy to integrate with marimo notebooks
- ✅ No complex build setup required

**Decorator specifically**:
- ✅ Most Pythonic syntax
- ✅ Self-documenting (Mojo code in docstring)
- ✅ Type hints work naturally
- ✅ Same performance as explicit caching

### Future Enhancement

A fourth approach could compile Mojo to Python extension modules (.so files):
- Zero subprocess overhead (~0.01-0.1ms per call vs current 10-50ms)
- Best for production with very frequent calls (1000s+)
- Requires more complex build setup (PyInit wrapper generation)

## Example Notebooks

- `example_notebook.py` — Interactive demo with reactive UI
- `benchmark_notebook.py` — Comprehensive comparison of all three approaches
