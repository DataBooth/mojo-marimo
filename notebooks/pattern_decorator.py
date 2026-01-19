"""@mojo Decorator Pattern - Clean Mojo functions in Python notebooks.

Run: marimo edit pattern_decorator.py
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
    # @mojo Decorator Pattern 🔥

    Write Mojo code in a function's docstring, call it like Python.

    ## Key Concept

    ```python
    @mojo
    def my_func(n: int) -> int:
        '''
        fn my_func(n: Int) -> Int:
            return n * n

        fn main():
            print(my_func({{n}}))
        '''
        ...

    result = my_func(10)  # Returns: 100
    ```

    Use `{{parameter}}` for substitution.
    """)
    return


@app.cell
def _():
    from mojo_marimo import mojo, get_mojo_version
    return get_mojo_version, mojo


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
    ## Example 1: Fibonacci
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
def _(fibonacci, mo):
    # Simple function calls
    result_10 = fibonacci(10)
    result_20 = fibonacci(20)

    mo.md(f"""
    ```python
    fibonacci(10) = {result_10}
    fibonacci(20) = {result_20:,}
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Example 2: Sum of Squares
    """)
    return


@app.cell
def _(mojo):
    @mojo
    def sum_squares(n: int) -> int:
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
    return (sum_squares,)


@app.cell
def _(mo, sum_squares):
    # Calculate sum: 1² + 2² + ... + 10²
    result = sum_squares(10)

    mo.md(f"""
    ```python
    sum_squares(10) = {result}  # 1² + 2² + ... + 10²
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Example 3: Prime Checker (Boolean)
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
def _(is_prime, mo):
    # Test some numbers
    primes_status = [
        (17, is_prime(17)),
        (18, is_prime(18)),
        (97, is_prime(97)),
        (100, is_prime(100)),
    ]

    results = "\n".join([f"{n}: {'✅ prime' if p else '❌ not prime'}" 
                         for n, p in primes_status])

    mo.md(f"""
    ```python
    {results}
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Example 4: Multiple Parameters
    """)
    return


@app.cell
def _(mojo):
    @mojo
    def gcd(a: int, b: int) -> int:
        """
        fn gcd(a: Int, b: Int) -> Int:
            var x = a
            var y = b
            while y != 0:
                var temp = y
                y = x % y
                x = temp
            return x

        fn main():
            print(gcd({{a}}, {{b}}))
        """
        ...
    return (gcd,)


@app.cell
def _(gcd, mo):
    # Test GCD with various inputs
    result_48_18 = gcd(48, 18)
    result_100_35 = gcd(100, 35)

    mo.md(f"""
    ```python
    gcd(48, 18) = {result_48_18}
    gcd(100, 35) = {result_100_35}
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Validation & Error Handling
    
    The decorator validates Mojo code **before** compilation to catch common errors early.
    
    **Validation checks:**
    - Missing `fn main()` function
    - Statements at file scope (e.g., `var x = 10` outside functions)
    - Missing colons after function declarations
    - Mixed tabs and spaces in indentation
    - Empty code
    - Deprecated `let` keyword (use `var` instead)
    - Python 2 style `print` without parentheses
    - Lowercase type names (`int` → `Int`, `str` → `String`, `bool` → `Bool`)
    - Missing parentheses in function calls (`range 10` → `range(10)`)
    
    See `pattern_executor.py` for detailed error examples.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    **Benefits:**
    - ✅ Clean Python-like API
    - ✅ Mojo code visible in notebook
    - ✅ Automatic type conversion
    - ✅ Cached execution (~10-50ms after first compile)
    - ✅ Pre-compilation validation with helpful hints

    **When to use:**
    - Self-contained Mojo functions
    - Interactive notebooks
    - Quick prototyping

    **See also:** `pattern_executor.py` for dynamic code generation and detailed validation examples
    """)
    return


if __name__ == "__main__":
    app.run()
