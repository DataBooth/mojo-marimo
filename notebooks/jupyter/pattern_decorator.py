# %% [markdown]
# # @mojo Decorator Pattern 🔥
#
# Write Mojo code in a function's docstring, call it like Python.
#
# ## Key Concept
#
# ```python
# @mojo
# def my_func(n: int) -> int:
#     '''
#     def my_func(n: Int) -> Int:
#         return n * n
#
#     def main():
#         print(my_func({{n}}))
#     '''
#     ...
#
# result = my_func(10)  # Returns: 100
# ```
#
# Use `{{parameter}}` for substitution.

# %%
from py_run_mojo import get_mojo_version, mojo

print(f"Mojo version: {get_mojo_version()}")

# %% [markdown]
# ## Example 1: Fibonacci


# %%
@mojo
def fibonacci(n: int) -> int:
    """
    def fibonacci(n: Int) -> Int:
        if n <= 1:
            return n
        var prev: Int = 0
        var curr: Int = 1
        for _ in range(2, n + 1):
            var next_val = prev + curr
            prev = curr
            curr = next_val
        return curr

    def main():
        print(fibonacci({{n}}))
    """
    ...


# Test the function
print(f"fibonacci(10) = {fibonacci(10)}")
print(f"fibonacci(20) = {fibonacci(20):,}")

# %% [markdown]
# ## Example 2: Sum of Squares


# %%
@mojo
def sum_squares(n: int) -> int:
    """
    def sum_squares(n: Int) -> Int:
        var total: Int = 0
        for i in range(1, n + 1):
            total += i * i
        return total

    def main():
        print(sum_squares({{n}}))
    """
    ...


# Calculate sum: 1² + 2² + ... + 10²
result = sum_squares(10)
print(f"sum_squares(10) = {result}  # 1² + 2² + ... + 10²")

# %% [markdown]
# ## Example 3: Prime Checker (Boolean)


# %%
@mojo
def is_prime(n: int) -> bool:
    """
    def is_prime(n: Int) -> Bool:
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

    def main():
        print(is_prime({{n}}))
    """
    ...


# Test some numbers
test_numbers = [17, 18, 97, 100]
for n in test_numbers:
    result = is_prime(n)
    status = "✅ prime" if result else "❌ not prime"
    print(f"{n}: {status}")

# %% [markdown]
# ## Performance Characteristics
#
# - **First call**: ~1-2 seconds (compiles Mojo code)
# - **Subsequent calls**: ~10-50ms (uses cached binary)
# - **Cache location**: `~/.mojo_cache/binaries/`
#
# The decorator pattern provides clean Python-like syntax while maintaining Mojo performance through intelligent caching.
