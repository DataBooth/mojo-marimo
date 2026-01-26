"""Interactive Mojo Learning - Explore Mojo with marimo's fast feedback loops.

For newcomers: experiment with Mojo interactively!
Run: marimo edit interactive_learning.py
"""

import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Interactive Mojo Learning 🎓

    Explore Mojo with **instant feedback** using marimo's reactivity.

    Change values with sliders → Mojo recompiles & runs → See results immediately!
    """)
    return


@app.cell
def _():
    from mojo_marimo import get_mojo_version, mojo, run_mojo

    return get_mojo_version, mojo, run_mojo


@app.cell
def _(get_mojo_version, mo):
    mo.md(f"""
    **Mojo:** `{get_mojo_version()}`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Experiment 1: Fibonacci - See How Performance Scales

    Try different values and watch execution time!
    """)
    return


@app.cell
def _(mojo):
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

    return (fibonacci,)


@app.cell
def _(mo):
    fib_n = mo.ui.slider(1, 45, value=10, label="n:", show_value=True)
    return (fib_n,)


@app.cell
def _(fib_n, fibonacci, mo):
    import time

    # Time the execution
    start = time.perf_counter()
    fib_result = fibonacci(fib_n.value)
    exec_time_ms = (time.perf_counter() - start) * 1000

    mo.md(f"""
    {fib_n}

    **Result:** `fibonacci({fib_n.value}) = {fib_result:,}`  
    **Execution:** `{exec_time_ms:.2f}ms` {"⚡ (cached!)" if exec_time_ms < 100 else "🔄 (compiling...)"}

    💡 *First run ~1-2s (compiling), subsequent runs ~10-50ms (cached)*
    """)
    return (time,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Experiment 2: Compare Algorithm Approaches

    Two ways to calculate sum of squares - which is faster?
    """)
    return


@app.cell
def _(mojo):
    @mojo
    def sum_squares_loop(n: int) -> int:
        """
        fn sum_squares(n: Int) -> Int:
            var total: Int = 0
            for i in range(1, n + 1):
                total += i * i
            return total

        fn main():
            print(sum_squares({{n}}))
        """
        ...

    @mojo
    def sum_squares_formula(n: int) -> int:
        """
        fn sum_squares_formula(n: Int) -> Int:
            # Formula: n(n+1)(2n+1)/6
            return (n * (n + 1) * (2 * n + 1)) // 6

        fn main():
            print(sum_squares_formula({{n}}))
        """
        ...

    return sum_squares_formula, sum_squares_loop


@app.cell
def _(mo):
    sum_n = mo.ui.slider(1, 100000, value=10000, label="n:", show_value=True, step=1000)
    return (sum_n,)


@app.cell
def _(mo, sum_n, sum_squares_formula, sum_squares_loop, time):
    # Benchmark both approaches
    start1 = time.perf_counter()
    result_loop = sum_squares_loop(sum_n.value)
    time_loop = (time.perf_counter() - start1) * 1000

    start2 = time.perf_counter()
    result_formula = sum_squares_formula(sum_n.value)
    time_formula = (time.perf_counter() - start2) * 1000

    speedup = time_loop / time_formula if time_formula > 0 else 0

    mo.md(f"""
    {sum_n}

    **Results:** Both = `{result_loop:,}` ✓

    | Approach | Time |
    |----------|------|
    | Loop | {time_loop:.3f}ms |
    | Formula (O(1)) | {time_formula:.3f}ms |

    **Speedup:** `{speedup:.1f}×` faster with mathematical formula!

    💡 *Loop is O(n), formula is O(1) - see the difference!*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Experiment 3: Explore Prime Number Patterns

    Interactive prime checking - discover patterns!
    """)
    return


@app.cell
def _(mojo):
    @mojo
    def is_prime(n: int) -> bool:
        """
        fn is_prime(n: Int) -> Bool:
            if n < 2:
                return False
            if n == 2:
                return True
            if n % 2 == 0:
                return False

            var i: Int = 3
            while i * i <= n:
                if n % i == 0:
                    return False
                i += 2

            return True

        fn main():
            print(is_prime({{n}}))
        """
        ...

    return (is_prime,)


@app.cell
def _(mo):
    prime_range = mo.ui.range_slider(1, 100, value=[1, 50], label="Range:", show_value=True)
    return (prime_range,)


@app.cell
def _(is_prime, mo, prime_range):
    # Find all primes in range
    start_val, end_val = prime_range.value
    primes = [n for n in range(start_val, end_val + 1) if is_prime(n)]
    prime_count = len(primes)
    density = (prime_count / (end_val - start_val + 1)) * 100 if end_val > start_val else 0

    mo.md(f"""
    {prime_range}

    **Primes found:** {prime_count} out of {end_val - start_val + 1} numbers ({density:.1f}%)

    **Prime list:** {", ".join(map(str, primes[:20]))}{"..." if len(primes) > 20 else ""}

    💡 *Prime density decreases as numbers get larger (Prime Number Theorem)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Experiment 4: Dynamic Code Generation

    Generate different Mojo operations on the fly!
    """)
    return


@app.cell
def _(mo):
    operation_choice = mo.ui.dropdown(
        ["add", "multiply", "power", "modulo"], value="add", label="Operation:"
    )

    val_a = mo.ui.number(1, 100, value=12, label="a:")
    val_b = mo.ui.number(1, 100, value=5, label="b:")

    mo.md(f"{operation_choice} {val_a} {val_b}")
    return operation_choice, val_a, val_b


@app.cell
def _(mo, operation_choice, run_mojo, time, val_a, val_b):
    # Map operations to Mojo expressions
    operations_map = {
        "add": ("a + b", "+"),
        "multiply": ("a * b", "×"),
        "power": ("a ** b", "^"),
        "modulo": ("a % b", "%"),
    }

    mojo_expr, symbol = operations_map[operation_choice.value]

    # Generate Mojo code dynamically
    dynamic_code = f"""
    fn compute(a: Int, b: Int) -> Int:
        return {mojo_expr}

    fn main():
        print(compute({val_a.value}, {val_b.value}))
    """

    # Execute
    start_dyn = time.perf_counter()
    result_dyn = int(run_mojo(dynamic_code))
    time_dyn = (time.perf_counter() - start_dyn) * 1000

    mo.md(f"""
    **Result:** `{val_a.value} {symbol} {val_b.value} = {result_dyn:,}`  
    **Time:** {time_dyn:.2f}ms

    <details>
    <summary>Generated Mojo code (click to expand)</summary>

    ```mojo
    {dynamic_code.strip()}
    ```
    </details>

    💡 *Each different operation generates new Mojo code - watch the compile time!*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## What You're Learning

    - **Instant Feedback** - Change slider → See results immediately
    - **Caching Benefits** - First compile ~1-2s, then ~10-50ms
    - **Algorithm Comparison** - O(n) vs O(1) performance
    - **Dynamic Code** - Generate Mojo on the fly
    - **Real Mojo Performance** - No Python fallbacks

    ## Next Steps

    - **pattern_decorator.py** - Learn the decorator pattern
    - **pattern_executor.py** - Learn dynamic code generation
    - **benchmarks.py** - Proper performance benchmarking

    ## Try Modifying

    1. Change the Fibonacci algorithm - try memoization!
    2. Implement different primality tests (Miller-Rabin?)
    3. Add more operations to the dynamic code generator
    4. Compare different sorting algorithms

    The key is **fast feedback** - make a change, see results instantly!
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
