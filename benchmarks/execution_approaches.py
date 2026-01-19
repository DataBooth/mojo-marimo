"""Mojo Execution Approaches: Comparison Benchmark.

Compares three approaches for running Mojo code:
1. Uncached executor (run_mojo directly)
2. Cached executor (examples module)
3. Decorator (@mojo)
"""

import marimo

__generated_with = "0.10.18"
app = marimo.App(width="medium")


@app.cell
def __():
    import statistics
    import sys
    import time
    from pathlib import Path

    import marimo as mo

    # Add benchmarks and examples to path
    bench_dir = Path(__file__).parent
    examples_dir = bench_dir.parent / "examples"
    sys.path.insert(0, str(bench_dir))
    sys.path.insert(0, str(examples_dir))

    return mo, time, statistics, Path, sys, bench_dir, examples_dir


@app.cell
def __(mo):
    mo.md(
        """
        # Mojo Execution Approaches: Benchmark
        
        This notebook compares three approaches for running Mojo code from Python:
        
        1. **Uncached executor**: Direct `run_mojo()` - recompiles every time
        2. **Cached executor**: Cached binary execution (examples module)
        3. **Decorator**: `@mojo` decorator - same caching as #2, cleaner syntax
        
        ## Performance expectations
        
        - **Uncached**: Slow every time (~1-2s per call)
        - **Cached (first call)**: Slow once (~1-2s), then fast
        - **Cached (subsequent)**: Fast (~10-50ms)
        - **Decorator**: Same as cached (uses same mechanism)
        """
    )
    return


@app.cell
def __():
    # Import all three approaches
    from uncached_executor import (
        fibonacci as fib_uncached,
        sum_squares as sum_sq_uncached,
        is_prime as prime_uncached,
    )
    from examples import (
        fibonacci as fib_cached,
        sum_squares as sum_sq_cached,
        is_prime as prime_cached,
    )
    from mojo_implementations import (
        fibonacci as fib_decorator,
        sum_squares as sum_sq_decorator,
        is_prime as prime_decorator,
    )
    from mojo_marimo import clear_cache

    return (
        fib_uncached,
        sum_sq_uncached,
        prime_uncached,
        fib_cached,
        sum_sq_cached,
        prime_cached,
        fib_decorator,
        sum_sq_decorator,
        prime_decorator,
        clear_cache,
    )


@app.cell
def __(mo):
    mo.md("## Benchmark Utility")
    return


@app.cell
def __(time, statistics):
    def benchmark_function(func, *args, warmup_runs=0, timed_runs=5):
        """Benchmark a function with warmup and multiple timed runs."""
        # Warmup
        for _ in range(warmup_runs):
            func(*args)

        # Timed runs
        times = []
        for _ in range(timed_runs):
            start = time.perf_counter()
            result = func(*args)
            elapsed = time.perf_counter() - start
            times.append(elapsed * 1000)  # Convert to ms

        return {
            "result": result,
            "mean_ms": statistics.mean(times),
            "stdev_ms": statistics.stdev(times) if len(times) > 1 else 0,
            "min_ms": min(times),
            "max_ms": max(times),
            "runs": len(times),
        }

    return (benchmark_function,)


@app.cell
def __(mo):
    mo.md("## Clear Cache & Cold Start Test")
    return


@app.cell
def __(clear_cache, mo):
    clear_cache()
    mo.md("✓ Cache cleared - next cached/decorator calls will be cold starts")
    return


@app.cell
def __(mo):
    mo.md("## Fibonacci(30) - Cold Start")
    return


@app.cell
def __(
    benchmark_function,
    fib_uncached,
    fib_cached,
    fib_decorator,
    mo,
):
    n = 30

    mo.md(f"### Testing fibonacci({n})...")

    # Uncached (always slow)
    bench_uncached = benchmark_function(fib_uncached, n, warmup_runs=0, timed_runs=3)
    mo.md(
        f"""
        **1. Uncached executor** (recompiles every time)
        - Mean: {bench_uncached['mean_ms']:.1f}ms ± {bench_uncached['stdev_ms']:.1f}ms
        - Result: {bench_uncached['result']}
        """
    )

    # Cached (first call is slow)
    bench_cached_cold = benchmark_function(fib_cached, n, warmup_runs=0, timed_runs=1)
    mo.md(
        f"""
        **2. Cached executor** (first call - compiles)
        - Time: {bench_cached_cold['mean_ms']:.1f}ms
        - Result: {bench_cached_cold['result']}
        """
    )

    # Decorator (first call is slow)
    bench_decorator_cold = benchmark_function(
        fib_decorator, n, warmup_runs=0, timed_runs=1
    )
    mo.md(
        f"""
        **3. Decorator** (first call - compiles)
        - Time: {bench_decorator_cold['mean_ms']:.1f}ms
        - Result: {bench_decorator_cold['result']}
        """
    )

    return bench_uncached, bench_cached_cold, bench_decorator_cold, n


@app.cell
def __(mo):
    mo.md("## Fibonacci(30) - Warm (Cached)")
    return


@app.cell
def __(
    benchmark_function,
    fib_uncached,
    fib_cached,
    fib_decorator,
    n,
    mo,
):
    mo.md(f"### Testing fibonacci({n}) with warm cache...")

    # Uncached (still slow)
    bench_uncached_warm = benchmark_function(
        fib_uncached, n, warmup_runs=1, timed_runs=5
    )
    mo.md(
        f"""
        **1. Uncached executor** (still recompiles)
        - Mean: {bench_uncached_warm['mean_ms']:.1f}ms ± {bench_uncached_warm['stdev_ms']:.1f}ms
        """
    )

    # Cached (now fast!)
    bench_cached_warm = benchmark_function(fib_cached, n, warmup_runs=1, timed_runs=5)
    mo.md(
        f"""
        **2. Cached executor** (using cached binary)
        - Mean: {bench_cached_warm['mean_ms']:.1f}ms ± {bench_cached_warm['stdev_ms']:.1f}ms
        - **Speedup vs uncached: {bench_uncached_warm['mean_ms'] / bench_cached_warm['mean_ms']:.1f}x**
        """
    )

    # Decorator (now fast!)
    bench_decorator_warm = benchmark_function(
        fib_decorator, n, warmup_runs=1, timed_runs=5
    )
    mo.md(
        f"""
        **3. Decorator** (using cached binary)
        - Mean: {bench_decorator_warm['mean_ms']:.1f}ms ± {bench_decorator_warm['stdev_ms']:.1f}ms
        - **Speedup vs uncached: {bench_uncached_warm['mean_ms'] / bench_decorator_warm['mean_ms']:.1f}x**
        """
    )

    return bench_uncached_warm, bench_cached_warm, bench_decorator_warm


@app.cell
def __(mo):
    mo.md("## Summary")
    return


@app.cell
def __(mo, bench_cached_warm, bench_decorator_warm):
    mo.md(
        f"""
        ### Performance Summary
        
        **Cached executor** and **Decorator** have identical performance 
        (both use the same caching mechanism):
        - Cached: {bench_cached_warm['mean_ms']:.1f}ms
        - Decorator: {bench_decorator_warm['mean_ms']:.1f}ms
        
        ### Recommendations
        
        **Use Uncached Executor when:**
        - Rapid prototyping
        - Code changes frequently
        - Single-use scripts
        
        **Use Cached Executor when:**
        - Need explicit cache control
        - Running same code repeatedly
        - Prefer explicit over implicit
        
        **Use Decorator when:**
        - Want clean, Pythonic syntax
        - Same code runs multiple times
        - Prefer self-documenting code
        - **Best choice for most use cases**
        """
    )
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
