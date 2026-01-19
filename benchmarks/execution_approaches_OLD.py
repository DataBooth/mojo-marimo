"""Benchmark and comparison of two Mojo execution approaches.

Compares:
1. Cached binary (examples.py via executor.py)
2. Decorator (decorator.py)

Measures:
- First call overhead (compilation time)
- Subsequent call overhead (execution time)
- Usability/ergonomics
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

    # Add src directory to path
    src_dir = Path(__file__).parent
    sys.path.insert(0, str(src_dir))
    return mo, time, statistics, Path, sys, src_dir


@app.cell
def __(mo):
    mo.md(
        """
        # Mojo Execution Approaches: Comparison & Benchmark
        
        This notebook compares two practical approaches for running Mojo code from Python/marimo:
        
        1. **Cached binary** (via examples): Explicit caching, clear control
        2. **Decorator**: Same performance, cleaner Pythonic syntax
        
        Both use the same underlying caching mechanism, so performance is identical.
        
        We'll test each approach on the same computational tasks and measure:
        - First-call latency (compilation + execution)
        - Subsequent-call latency (execution only)
        - Usability (code ergonomics)
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## Test Functions")
    return


@app.cell
def __(mo):
    mo.md(
        """
        We'll test three functions of varying complexity:
        - `fibonacci(10)` — simple recursive-like iteration
        - `sum_squares(100)` — simple loop with arithmetic
        - `is_prime(104729)` — moderate computational work
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## Approach 1: Cached Binary (Examples)")
    return


@app.cell
def __(mo):
    mo.md(
        """
        **Pattern**: First call compiles to binary and caches by source hash, subsequent calls reuse binary.
        
        **Pros**:
        - Fast subsequent calls (10-50ms)
        - Good for repeated execution
        - Cache persists across sessions
        
        **Cons**:
        - First call overhead (~1-2s)
        - Still subprocess overhead
        - Manual function wrapping
        """
    )
    return


@app.cell
def __():
    # Add examples to path
    import sys
    from pathlib import Path

    examples_path = Path(__file__).parent.parent / "examples"
    sys.path.insert(0, str(examples_path))

    from examples import (
        fibonacci as fib_cached,
    )
    from examples import (
        is_prime as prime_cached,
    )
    from examples import (
        sum_squares as sum_sq_cached,
    )
    from mojo_marimo.executor import clear_cache

    return clear_cache, fib_cached, prime_cached, sum_sq_cached


@app.cell
def __(mo):
    mo.md("## Approach 2: Decorator")
    return


@app.cell
def __(mo):
    mo.md(
        """
        **Pattern**: Decorator extracts Mojo code from docstring, uses cached binary execution.
        
        **Pros**:
        - Clean, Pythonic syntax
        - Self-documenting (Mojo code in docstring)
        - Same performance as cached binary
        
        **Cons**:
        - Requires decorator setup
        - Still subprocess overhead
        - Future enhancement: compile to .so for zero subprocess overhead
        """
    )
    return


@app.cell
def __():
    from mojo_marimo.decorator import (
        fibonacci as fib_decorator,
    )
    from mojo_marimo.decorator import (
        is_prime as prime_decorator,
    )
    from mojo_marimo.decorator import (
        sum_squares as sum_sq_decorator,
    )

    return fib_decorator, prime_decorator, sum_sq_decorator


@app.cell
def __(mo):
    mo.md("## Benchmark Setup")
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
    mo.md("## Run Benchmarks")
    return


@app.cell
def __(mo):
    mo.md("### First: Clear cache to measure cold start")
    return


@app.cell
def __(clear_cache):
    # Clear cache to ensure we measure first-call performance
    clear_cache()
    print("Cache cleared")
    return


@app.cell
def __(mo):
    mo.md("### Fibonacci(10) - Cold Start")
    return


@app.cell
def __(benchmark_function, fib_uncached, fib_cached, fib_decorator):
    fib_n = 10

    print("Testing fibonacci(10)...\n")

    # First call (cold start) - no warmup
    print("1. Uncached subprocess (cold):")
    bench_fib_uncached_cold = benchmark_function(fib_uncached, fib_n, warmup_runs=0, timed_runs=3)
    print(
        f"   Mean: {bench_fib_uncached_cold['mean_ms']:.2f}ms ± {bench_fib_uncached_cold['stdev_ms']:.2f}ms"
    )
    print(f"   Result: {bench_fib_uncached_cold['result']}\n")

    print("2. Cached binary (cold, first compile):")
    bench_fib_cached_cold = benchmark_function(fib_cached, fib_n, warmup_runs=0, timed_runs=1)
    print(f"   Time: {bench_fib_cached_cold['mean_ms']:.2f}ms")
    print(f"   Result: {bench_fib_cached_cold['result']}\n")

    print("3. Decorator (cold, first compile):")
    bench_fib_decorator_cold = benchmark_function(fib_decorator, fib_n, warmup_runs=0, timed_runs=1)
    print(f"   Time: {bench_fib_decorator_cold['mean_ms']:.2f}ms")
    print(f"   Result: {bench_fib_decorator_cold['result']}")
    return (
        bench_fib_cached_cold,
        bench_fib_decorator_cold,
        bench_fib_uncached_cold,
        fib_n,
    )


@app.cell
def __(mo):
    mo.md("### Fibonacci(10) - Warm (Cached)")
    return


@app.cell
def __(benchmark_function, fib_uncached, fib_cached, fib_decorator, fib_n):
    print("Testing fibonacci(10) - cached...\n")

    # Warm calls (cached)
    print("1. Uncached subprocess (still compiles every time):")
    bench_fib_uncached_warm = benchmark_function(fib_uncached, fib_n, warmup_runs=1, timed_runs=5)
    print(
        f"   Mean: {bench_fib_uncached_warm['mean_ms']:.2f}ms ± {bench_fib_uncached_warm['stdev_ms']:.2f}ms\n"
    )

    print("2. Cached binary (using cached binary):")
    bench_fib_cached_warm = benchmark_function(fib_cached, fib_n, warmup_runs=1, timed_runs=5)
    print(
        f"   Mean: {bench_fib_cached_warm['mean_ms']:.2f}ms ± {bench_fib_cached_warm['stdev_ms']:.2f}ms\n"
    )

    print("3. Decorator (using cached binary):")
    bench_fib_decorator_warm = benchmark_function(fib_decorator, fib_n, warmup_runs=1, timed_runs=5)
    print(
        f"   Mean: {bench_fib_decorator_warm['mean_ms']:.2f}ms ± {bench_fib_decorator_warm['stdev_ms']:.2f}ms"
    )
    return bench_fib_cached_warm, bench_fib_decorator_warm, bench_fib_uncached_warm


@app.cell
def __(mo):
    mo.md("### Sum Squares(100) - Warm")
    return


@app.cell
def __(
    benchmark_function,
    sum_sq_uncached,
    sum_sq_cached,
    sum_sq_decorator,
):
    sum_n = 100

    print("Testing sum_squares(100) - warm...\n")

    print("1. Uncached subprocess:")
    bench_sum_uncached = benchmark_function(sum_sq_uncached, sum_n, warmup_runs=1, timed_runs=5)
    print(
        f"   Mean: {bench_sum_uncached['mean_ms']:.2f}ms ± {bench_sum_uncached['stdev_ms']:.2f}ms"
    )
    print(f"   Result: {bench_sum_uncached['result']}\n")

    print("2. Cached binary:")
    bench_sum_cached = benchmark_function(sum_sq_cached, sum_n, warmup_runs=1, timed_runs=5)
    print(f"   Mean: {bench_sum_cached['mean_ms']:.2f}ms ± {bench_sum_cached['stdev_ms']:.2f}ms")
    print(f"   Result: {bench_sum_cached['result']}\n")

    print("3. Decorator:")
    bench_sum_decorator = benchmark_function(sum_sq_decorator, sum_n, warmup_runs=1, timed_runs=5)
    print(
        f"   Mean: {bench_sum_decorator['mean_ms']:.2f}ms ± {bench_sum_decorator['stdev_ms']:.2f}ms"
    )
    print(f"   Result: {bench_sum_decorator['result']}")
    return bench_sum_cached, bench_sum_decorator, bench_sum_uncached, sum_n


@app.cell
def __(mo):
    mo.md("### Is Prime(104729) - Warm")
    return


@app.cell
def __(benchmark_function, prime_uncached, prime_cached, prime_decorator):
    prime_n = 104729  # 10,000th prime

    print("Testing is_prime(104729) - warm...\n")

    print("1. Uncached subprocess:")
    bench_prime_uncached = benchmark_function(prime_uncached, prime_n, warmup_runs=1, timed_runs=5)
    print(
        f"   Mean: {bench_prime_uncached['mean_ms']:.2f}ms ± {bench_prime_uncached['stdev_ms']:.2f}ms"
    )
    print(f"   Result: {bench_prime_uncached['result']}\n")

    print("2. Cached binary:")
    bench_prime_cached = benchmark_function(prime_cached, prime_n, warmup_runs=1, timed_runs=5)
    print(
        f"   Mean: {bench_prime_cached['mean_ms']:.2f}ms ± {bench_prime_cached['stdev_ms']:.2f}ms"
    )
    print(f"   Result: {bench_prime_cached['result']}\n")

    print("3. Decorator:")
    bench_prime_decorator = benchmark_function(
        prime_decorator, prime_n, warmup_runs=1, timed_runs=5
    )
    print(
        f"   Mean: {bench_prime_decorator['mean_ms']:.2f}ms ± {bench_prime_decorator['stdev_ms']:.2f}ms"
    )
    print(f"   Result: {bench_prime_decorator['result']}")
    return bench_prime_cached, bench_prime_decorator, bench_prime_uncached, prime_n


@app.cell
def __(mo):
    mo.md("## Summary & Visualisation")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ### Performance Summary
        
        The table below shows mean execution times for each approach:
        """
    )
    return


@app.cell
def __(
    mo,
    bench_fib_uncached_warm,
    bench_fib_cached_warm,
    bench_fib_decorator_warm,
    bench_sum_uncached,
    bench_sum_cached,
    bench_sum_decorator,
    bench_prime_uncached,
    bench_prime_cached,
    bench_prime_decorator,
):
    summary_data = [
        {
            "Function": "fibonacci(10)",
            "Uncached (ms)": f"{bench_fib_uncached_warm['mean_ms']:.2f}",
            "Cached (ms)": f"{bench_fib_cached_warm['mean_ms']:.2f}",
            "Decorator (ms)": f"{bench_fib_decorator_warm['mean_ms']:.2f}",
        },
        {
            "Function": "sum_squares(100)",
            "Uncached (ms)": f"{bench_sum_uncached['mean_ms']:.2f}",
            "Cached (ms)": f"{bench_sum_cached['mean_ms']:.2f}",
            "Decorator (ms)": f"{bench_sum_decorator['mean_ms']:.2f}",
        },
        {
            "Function": "is_prime(104729)",
            "Uncached (ms)": f"{bench_prime_uncached['mean_ms']:.2f}",
            "Cached (ms)": f"{bench_prime_cached['mean_ms']:.2f}",
            "Decorator (ms)": f"{bench_prime_decorator['mean_ms']:.2f}",
        },
    ]

    mo.ui.table(summary_data)
    return (summary_data,)


@app.cell
def __(mo):
    mo.md(
        """
        ### Recommendations
        
        **Use uncached subprocess when**:
        - Rapid prototyping / development
        - Code changes frequently
        - Don't need optimal performance
        
        **Use cached binary when**:
        - Running same Mojo code repeatedly
        - Need better performance than uncached
        - Willing to manage caching explicitly
        
        **Use decorator when**:
        - Want clean, Pythonic syntax
        - Same performance as cached binary
        - Prefer self-documenting code (Mojo in docstrings)
        
        **Future: Python extension approach**:
        - For production with very frequent calls (1000s+)
        - Would eliminate subprocess overhead entirely
        - Requires more complex build setup
        - Expected: ~0.01-0.1ms per call vs current 10-50ms
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## Code Comparison")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ### Usability Comparison
        
        Here's how the same functionality looks in each approach:
        """
    )
    return


@app.cell
def __(mo):
    code_comparison = mo.md('''
        **Approach 1: Uncached Subprocess**
        ```python
        # compute_wrapper.py
        def fibonacci(n: int) -> int:
            mojo_code = f"""
            fn fibonacci(n: Int) -> Int:
                # ... mojo implementation ...
            fn main():
                print(fibonacci({n}))
            """
            return int(mo_run_mojo(mojo_code))
        
        # Usage
        result = fibonacci(10)
        ```
        
        **Approach 2: Cached Binary**
        ```python
        # mo_run_cached.py
        def fibonacci_cached(n: int) -> int:
            mojo_code = f"""
            fn fibonacci(n: Int) -> Int:
                # ... mojo implementation ...
            fn main():
                print(fibonacci({n}))
            """
            return int(mo_run_mojo_cached(mojo_code))
        
        # Usage
        result = fibonacci_cached(10)
        ```
        
        **Approach 3: Decorator**
        ```python
        # mojo_decorator.py
        @mojo
        def fibonacci(n: int) -> int:
            """
            fn fibonacci(n: Int) -> Int:
                # ... mojo implementation ...
            fn main():
                print(fibonacci({{n}}))
            """
            pass
        
        # Usage (looks like normal Python!)
        result = fibonacci(10)
        ```
    ''')
    code_comparison
    return (code_comparison,)


@app.cell
def __(mo):
    mo.md(
        """
        ### Winner: Decorator for Usability
        
        The decorator approach provides:
        - Most Pythonic syntax
        - Self-documenting (Mojo code visible in source)
        - Type hints work naturally
        - Clean separation of interface and implementation
        - Same performance as cached binary
        """
    )
    return


@app.cell
def __():
    # Export marker for marimo
    return


if __name__ == "__main__":
    app.run()
