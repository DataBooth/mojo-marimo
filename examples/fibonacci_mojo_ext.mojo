"""Mojo extension module demonstrating .so compilation approach.

This shows the alternative to mojo-marimo's subprocess pattern.

Compile manually:
    mojo build fibonacci_mojo_ext.mojo --emit shared-lib

Or use auto-compilation:
    import mojo.importer
    import fibonacci_mojo_ext
    result = fibonacci_mojo_ext.fibonacci(10)
"""

from python import PythonObject
from python.bindings import PythonModuleBuilder
from os import abort


@export
fn PyInit_fibonacci_mojo_ext() -> PythonObject:
    """Initialize the Python extension module.
    
    Python looks for PyInit_<module_name>() when importing.
    """
    try:
        var mb = PythonModuleBuilder("fibonacci_mojo_ext")
        mb.def_function[fibonacci](
            "fibonacci",
            docstring="Calculate nth Fibonacci number (iterative)"
        )
        mb.def_function[is_prime](
            "is_prime", 
            docstring="Check if number is prime"
        )
        return mb.finalize()
    except e:
        print("error creating Python Mojo module:", e)
        return PythonObject()


fn fibonacci(py_n: PythonObject) raises -> PythonObject:
    """Calculate nth Fibonacci number.
    
    Note: Takes PythonObject, not native Mojo Int.
    This is required for Python extension module functions.
    """
    var n = Int(py_n)
    
    if n <= 1:
        return PythonObject(n)
    
    var prev: Int = 0
    var curr: Int = 1
    
    for _ in range(2, n + 1):
        var next_val = prev + curr
        prev = curr
        curr = next_val
    
    return PythonObject(curr)


fn is_prime(py_n: PythonObject) raises -> PythonObject:
    """Check if number is prime using trial division."""
    var n = Int(py_n)
    
    if n < 2:
        return PythonObject(False)
    if n == 2:
        return PythonObject(True)
    if n % 2 == 0:
        return PythonObject(False)
    
    var i: Int = 3
    while i * i <= n:
        if n % i == 0:
            return PythonObject(False)
        i += 2
    
    return PythonObject(True)
