# Mojo Extension Modules (.so approach)

This directory contains an example of the **alternative approach** to integrating Mojo with Python: compiling Mojo code to Python extension modules (`.so` files) that can be imported directly.

## Two Approaches Compared

### Approach 1: Subprocess Execution (Current mojo-marimo)

**How it works:**
```python
from mojo_marimo import mojo

@mojo
def fibonacci(n: int) -> int:
    """
    fn fibonacci(n: Int) -> Int:
        # Mojo implementation
    """
    ...

result = fibonacci(10)  # Compiles, caches, runs subprocess
```

**Pros:**
- ✅ Simple - minimal boilerplate
- ✅ Clean API - native Python types
- ✅ Works today with no extra setup
- ✅ Easy to understand and debug

**Cons:**
- ❌ Subprocess overhead (~10-50ms per call)
- ❌ Not suitable for tight loops with thousands of calls

### Approach 2: Extension Modules (.so files)

**How it works:**
```bash
# 1. Write Mojo with Python bindings
# See fibonacci_mojo_ext.mojo

# 2. Compile to shared library
mojo build fibonacci_mojo_ext.mojo --emit shared-lib

# 3. Import in Python
import mojo.importer  # Enables auto-compilation
import fibonacci_mojo_ext

result = fibonacci_mojo_ext.fibonacci(10)  # Direct call!
```

**Pros:**
- ✅ Zero subprocess overhead
- ✅ Direct Python imports
- ✅ Suitable for performance-critical tight loops
- ✅ Auto-compilation with `mojo.importer`

**Cons:**
- ❌ More complex Mojo code (requires `PythonModuleBuilder`)
- ❌ Functions must take `PythonObject` arguments
- ❌ Need `PyInit_*()` boilerplate
- ❌ Steeper learning curve

## Example: Extension Module

See [`fibonacci_mojo_ext.mojo`](./fibonacci_mojo_ext.mojo) for a complete example with:
- `fibonacci()` function
- `is_prime()` function
- Proper `PyInit_*()` setup
- `PythonModuleBuilder` configuration

### Manual Compilation

```bash
# Compile to .so
mojo build fibonacci_mojo_ext.mojo --emit shared-lib -o fibonacci_mojo_ext.so

# Use in Python
python -c "
import fibonacci_mojo_ext
print(fibonacci_mojo_ext.fibonacci(10))
print(fibonacci_mojo_ext.is_prime(17))
"
```

### Auto-Compilation (Recommended)

```python
import mojo.importer  # Enables import hook

# Automatically compiles .mojo file to .so when imported
# Caches in __mojocache__/ directory
import fibonacci_mojo_ext

print(fibonacci_mojo_ext.fibonacci(10))
```

### Interactive Notebook

See [`notebooks/pattern_extension.py`](../notebooks/pattern_extension.py) for a complete marimo notebook demonstrating:
- Auto-compilation with `mojo.importer`
- Interactive examples with sliders
- Performance comparison with decorator pattern
- Direct benchmarking

## When to Use Each Approach

### Use Subprocess (Current mojo-marimo)

- ✅ Prototyping and development
- ✅ Educational notebooks
- ✅ Compute-intensive tasks (>100ms)
- ✅ When simplicity > absolute performance
- ✅ Interactive notebooks with fast iteration

### Use Extension Modules

- ✅ Production deployments
- ✅ Functions called thousands of times
- ✅ Performance-critical tight loops
- ✅ When every millisecond counts
- ✅ Stable APIs that don't change often

## Performance Comparison

### Subprocess Approach
```python
# First call: ~1-2s (compile + run)
# Subsequent: ~10-50ms (subprocess overhead + computation)
```

### Extension Module Approach
```python
# First call: ~1-2s (compile .so)
# Subsequent: ~0.01-0.1ms (direct function call + computation)
```

**Key difference:** Extension modules eliminate the 10-50ms subprocess overhead, making them 100-1000x faster for simple operations or tight loops.

## Future Enhancement for mojo-marimo

The `mojo-marimo` library could potentially support both modes:

```python
from mojo_marimo import mojo

# Subprocess mode (current, simple)
@mojo(mode="subprocess")
def fibonacci_simple(n: int) -> int:
    """..."""
    ...

# Extension mode (future, zero overhead)
@mojo(mode="extension")
def fibonacci_fast(n: int) -> int:
    """..."""
    ...
```

The decorator could automatically:
1. Generate the `PyInit_*()` boilerplate
2. Handle `PythonObject` conversions
3. Compile to `.so` with caching
4. Manage the `__mojocache__` directory

## Technical Details

### Required Mojo Code Structure

Extension modules need:

1. **Export function** with specific name:
```mojo
@export
fn PyInit_<module_name>() -> PythonObject:
    ...
```

2. **PythonModuleBuilder** to register functions:
```mojo
var mb = PythonModuleBuilder("module_name")
mb.def_function[my_function]("my_function")
return mb.finalize()
```

3. **Functions accepting PythonObject**:
```mojo
fn my_function(py_arg: PythonObject) raises -> PythonObject:
    var arg = Int(py=py_arg)  # Convert from Python
    var result = arg * 2
    return PythonObject(result)  # Convert to Python
```

### Cache Management

With `mojo.importer`, compiled `.so` files are cached in `__mojocache__/`:

```
project/
├── my_module.mojo
└── __mojocache__/
    └── my_module.hash-ABC123.so
```

Delete `__mojocache__/` to force recompilation.

## References

- [Mojo Documentation: Calling Mojo from Python](https://docs.modular.com/mojo/manual/python/mojo-from-python/)
- [PythonModuleBuilder API](https://docs.modular.com/mojo/stdlib/python/bindings/)
- [Compiled Languages Integration Guide](../docs/COMPILED_LANGUAGES.md)
