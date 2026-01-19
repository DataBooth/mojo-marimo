# Announcing mojo-marimo: Run Mojo in Interactive Python Notebooks 🔥

I'm excited to share **mojo-marimo** - a library that lets you run real Mojo code inside interactive Python notebooks using marimo.

## What is it?

`mojo-marimo` provides two clean patterns for executing high-performance Mojo code from Python/marimo notebooks:

### Pattern 1: @mojo Decorator (Cleanest)
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
result = fibonacci(10)  # Returns: 55
```

### Pattern 2: run_mojo() Executor
```python
from mojo_marimo import run_mojo

# Option A: Inline Mojo code
mojo_code = """
fn compute(n: Int) -> Int:
    return n * n

fn main():
    print(compute(42))
"""
result = run_mojo(mojo_code)

# Option B: Execute .mojo files
result = run_mojo("path/to/module.mojo")
```

## Key Features

✅ **Real Mojo Performance** - No Python fallbacks, actual Mojo execution  
✅ **Smart Caching** - SHA256-based binary caching (~1-2s first call, ~10-50ms cached)  
✅ **Type Safe** - Automatic type conversion (int, bool, float)  
✅ **Reactive** - Works perfectly with marimo's reactivity  
✅ **Two Patterns** - Decorator for clean code, executor for flexibility  
✅ **Interactive Examples** - Sliders, buttons, dropdowns with live Mojo execution  

## Why This Matters

Python notebooks are brilliant for exploration but hit a wall when you need serious performance. With `mojo-marimo`, you can:

- Prototype high-performance algorithms interactively
- Benchmark Mojo vs Python side-by-side
- Build interactive demos with real Mojo performance
- Explore Mojo features with immediate visual feedback

## Try It Out

**Installation:**
```bash
git clone https://github.com/DataBooth/mojo-marimo
cd mojo-marimo
uv sync --extra dev

# Or with just
just install
```

**Run the notebooks:**
```bash
# Decorator pattern examples
just notebook-decorator

# Executor pattern examples
just notebook-executor

# Benchmark comparison
just notebook-benchmark
```

## Technical Details

- **Caching:** Mojo code is compiled to binaries cached in `~/.mojo_cache/binaries/`
- **Cache Key:** SHA256 hash of source code
- **Recompilation:** Automatic when code changes
- **Environment:** Works with both `uv` and `pixi`

## Repository

🔗 https://github.com/DataBooth/mojo-marimo

Includes:
- 27 passing tests
- Comprehensive documentation
- Interactive notebooks demonstrating both patterns
- Benchmark notebook comparing performance
- Complete example implementations

## Feedback Welcome!

This is an early release (v0.1.0) and I'd love feedback from the Mojo community:

- Which pattern do you prefer and why?
- What use cases would benefit most?
- What features would you like to see?
- Any performance observations?

Looking forward to hearing your thoughts! Let me know if you try it out.

---

**Tech Stack:** Mojo, Python, marimo, uv  
**License:** Apache-2.0  
**Tested on:** macOS (Apple Silicon), Python 3.12-3.14, Mojo 0.25.7

