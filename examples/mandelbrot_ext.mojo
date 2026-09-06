"""
Mandelbrot Set Calculation - Python Extension Module
Provides zero-overhead Python callable functions using PythonModuleBuilder.
"""

from std.os import abort
from std.python import Python, PythonObject
from std.python.bindings import PythonModuleBuilder


@export
def PyInit_mandelbrot_ext() abi("C") -> PythonObject:
    """Initialize the Python extension module.

    Python looks for PyInit_<module_name>() when importing.
    """
    try:
        var mb = PythonModuleBuilder("mandelbrot_ext")
        # NOTE: def_py_function (not def_function) is required here because
        # compute_mandelbrot takes 7 arguments; def_function bindings support
        # at most 6 PythonObject arguments. def_py_function receives the raw
        # (self, args) pair instead.
        mb.def_py_function[compute_mandelbrot]("compute_mandelbrot")
        return mb.finalize()
    except e:
        abort(String("error creating Python Mojo module:", e))


def mandelbrot_point(cx: Float64, cy: Float64, max_iter: Int) -> Int:
    """Calculate iterations for a single point in the Mandelbrot set."""
    var x: Float64 = 0.0
    var y: Float64 = 0.0
    var iteration: Int = 0

    while x * x + y * y <= 4.0 and iteration < max_iter:
        var x_new = x * x - y * y + cx
        var y_new = 2.0 * x * y + cy
        x = x_new
        y = y_new
        iteration += 1

    return iteration


def compute_mandelbrot(py_self: PythonObject, py_args: PythonObject) raises -> PythonObject:
    """Compute the Mandelbrot set and return as nested list (2D array).

    Called from Python as:
        compute_mandelbrot(width, height, max_iter, x_min, x_max, y_min, y_max)

    Args:
        py_self: The module object (not used).
        py_args: Positional argument tuple:
            [0] width: Number of points in x direction.
            [1] height: Number of points in y direction.
            [2] max_iter: Maximum iterations per point.
            [3] x_min: Minimum real axis value.
            [4] x_max: Maximum real axis value.
            [5] y_min: Minimum imaginary axis value.
            [6] y_max: Maximum imaginary axis value.

    Returns:
        2D list of iteration counts (height x width).
    """
    var width = Int(py=py_args[0])
    var height = Int(py=py_args[1])
    var max_iter = Int(py=py_args[2])
    var x_min = Float64(py=py_args[3])
    var x_max = Float64(py=py_args[4])
    var y_min = Float64(py=py_args[5])
    var y_max = Float64(py=py_args[6])

    var dx = (x_max - x_min) / Float64(width)
    var dy = (y_max - y_min) / Float64(height)

    # Build result as nested Python list
    var result = Python.list()

    for row in range(height):
        var cy = y_min + Float64(row) * dy
        var row_data = Python.list()

        for col in range(width):
            var cx = x_min + Float64(col) * dx
            var iterations = mandelbrot_point(cx, cy, max_iter)
            _ = row_data.append(iterations)

        _ = result.append(row_data)

    return result
