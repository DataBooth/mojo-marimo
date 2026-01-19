"""Marimo notebook demonstrating the @mojo decorator pattern.

Run with: marimo edit decorator_notebook.py
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
    
    The **cleanest way** to write Mojo functions in Python notebooks.
    
    ## How It Works
    
    1. Write Mojo code in the function's docstring
    2. Use `{{parameter}}` syntax for parameter substitution
    3. Call like a normal Python function
    4. Get automatic caching and type conversion
    """)
    return


@app.cell
def _():
    from mojo_marimo import mojo, get_mojo_version
    return get_mojo_version, mojo


@app.cell
def _(get_mojo_version, mo):
    mo.md(f"**Mojo Version:** `{get_mojo_version()}`")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Example 1: Fibonacci
    
    Notice how the Mojo code is **visible right in the notebook**:
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
    fib_slider = mo.ui.slider(1, 40, value=10, label="n:", show_value=True)
    return (fib_slider,)


@app.cell
def _(fib_slider, fibonacci, mo):
    fib_result = fibonacci(fib_slider.value)
    mo.md(f"""
    {fib_slider}
    
    **Fibonacci({fib_slider.value})** = `{fib_result:,}`
    """)
    return (fib_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Example 2: Sum of Squares
    
    Same pattern, different computation:
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
def _(mo):
    sum_slider = mo.ui.slider(1, 100, value=10, label="n:", show_value=True)
    return (sum_slider,)


@app.cell
def _(mo, sum_slider, sum_squares):
    sum_result = sum_squares(sum_slider.value)
    mo.md(f"""
    {sum_slider}
    
    **Sum: 1² + 2² + ... + {sum_slider.value}²** = `{sum_result:,}`
    """)
    return (sum_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Example 3: Prime Number Checker
    
    Returns `bool` - automatic type conversion!
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
    prime_input = mo.ui.number(1, 10000, value=97, label="Number to check:")
    return (prime_input,)


@app.cell
def _(is_prime, mo, prime_input):
    is_prime_result = is_prime(prime_input.value)
    
    status = "✅ Prime" if is_prime_result else "❌ Not Prime"
    color = "green" if is_prime_result else "red"
    
    mo.md(f"""
    {prime_input}
    
    **{prime_input.value}** is <span style="color: {color}; font-weight: bold;">{status}</span>
    """)
    return color, is_prime_result, status


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Example 4: Multiple Parameters
    
    You can use multiple parameters with the decorator:
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
def _(mo):
    gcd_a = mo.ui.number(1, 1000, value=48, label="a:")
    gcd_b = mo.ui.number(1, 1000, value=18, label="b:")
    return gcd_a, gcd_b


@app.cell
def _(gcd, gcd_a, gcd_b, mo):
    gcd_result = gcd(gcd_a.value, gcd_b.value)
    mo.md(f"""
    {gcd_a} {gcd_b}
    
    **GCD({gcd_a.value}, {gcd_b.value})** = `{gcd_result}`
    """)
    return (gcd_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Key Benefits
    
    ✅ **Clean API** - Looks like normal Python  
    ✅ **Type Safe** - Automatic type conversion (int, bool, float)  
    ✅ **Cached** - First call ~1-2s, subsequent ~10-50ms  
    ✅ **Visible Code** - Mojo implementation right in the notebook  
    ✅ **Reactive** - Works perfectly with marimo's reactivity  
    
    ## Pattern Template
    
    ```python
    from mojo_marimo import mojo
    
    @mojo
    def my_function(param1: int, param2: int) -> int:
        '''
        fn my_function(p1: Int, p2: Int) -> Int:
            # Your Mojo code here
            return p1 + p2
        
        fn main():
            print(my_function({{param1}}, {{param2}}))
        '''
        ...
    
    # Call it like normal Python
    result = my_function(10, 20)
    ```
    
    ## When to Use
    
    - ✅ Self-contained Mojo functions
    - ✅ When you want code visible in notebook
    - ✅ Interactive notebooks and demos
    - ✅ Quick prototyping
    
    For larger Mojo modules, see `executor_notebook.py`
    """)
    return


if __name__ == "__main__":
    app.run()
