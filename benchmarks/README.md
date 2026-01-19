# Benchmarks

This directory contains benchmarking notebooks and implementations comparing Python and Mojo performance.

## Structure

- **`python_baseline.py`** - Pure Python implementations (no numpy/optimisations)
- **`mojo_implementations.py`** - Mojo implementations using `@mojo` decorator
- **`uncached_executor.py`** - Uncached Mojo executor (for measuring compilation overhead)
- **`python_vs_mojo.py`** - Interactive notebook comparing Python vs Mojo performance
- **`execution_approaches.py`** - Notebook comparing different Mojo execution approaches

## Running Benchmarks

### Python vs Mojo Performance
```bash
just benchmark
# or
pixi run benchmark
# or
uv run marimo edit benchmarks/python_vs_mojo.py
```

This notebook compares pure Python against Mojo implementations for:
- Fibonacci sequence
- Sum of squares
- Prime number testing
- Factorial
- GCD (Euclidean algorithm)
- Counting primes

**Expected results**: Mojo typically 2-100x faster depending on the algorithm.

### Execution Approaches
```bash
just benchmark-exec
# or
pixi run benchmark-exec
# or
uv run marimo edit benchmarks/execution_approaches.py
```

This notebook compares three ways to run Mojo code:
1. **Uncached executor** - Recompiles every time (~1-2s per call)
2. **Cached executor** - Compiles once, fast subsequent calls (~10-50ms)
3. **Decorator** - Same as cached, but cleaner syntax

## Algorithm Implementations

All algorithms are implemented identically in Python and Mojo for fair comparison:

### Fibonacci (iterative)
```python
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
```

### Sum of Squares
```python
def sum_squares(n: int) -> int:
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total
```

### Prime Testing
```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
```

## Performance Tips

1. **Warm up the cache**: First call compiles, subsequent calls are fast
2. **Use larger inputs**: Subprocess overhead is amortised better
3. **Batch operations**: Multiple calls benefit from caching
4. **Clear cache between tests**: `clear_cache()` for accurate benchmarking

## Adding New Benchmarks

To add a new algorithm:

1. Add Python implementation to `python_baseline.py`
2. Add Mojo implementation to `mojo_implementations.py`
3. Update notebooks to include the new function
4. Ensure implementations are algorithmically identical
