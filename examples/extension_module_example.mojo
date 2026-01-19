"""Example Mojo extension module that can be imported directly by Python.

This demonstrates the alternative approach to mojo-marimo's subprocess pattern.
Compile with: mojo build extension_module_example.mojo --emit shared-lib

Then in Python:
    import mojo.importer
    import extension_module_example
    result = extension_module_example.fibonacci(10)
"""

from python import PythonObject
from python.bindings import PythonModuleBuilder
from os import abort


@export
fn PyInit_extension_module_example() -> PythonObject:
    """Initialize the Python extension module.
    
    Python looks for PyInit_<module_name>() when importing.
    """
    try:
        var mb = PythonModuleBuilder("extension_module_example")
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
        abort(String("error creating Python Mojo module: ", e))


fn fibonacci(py_n: PythonObject) raises -> PythonObject:
    """Calculate nth Fibonacci number.
    
    Note: Takes PythonObject, not native Mojo Int.
    This is required for Python extension module functions.
    """
    var n = Int(py=py_n)
    
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
    var n = Int(py=py_n)
    
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
