"""
Monte Carlo Pi Estimation - Python Extension Module
Provides zero-overhead Python callable functions using PythonModuleBuilder.
"""

from std.math import sqrt
from std.os import abort
from std.python import Python, PythonObject
from std.python.bindings import PythonModuleBuilder
from std.random import random_float64


@export
def PyInit_monte_carlo_ext() abi("C") -> PythonObject:
    """Initialize the Python extension module.

    Python looks for PyInit_<module_name>() when importing.
    """
    try:
        var mb = PythonModuleBuilder("monte_carlo_ext")
        mb.def_function[estimate_pi](
            "estimate_pi",
            docstring="Estimate pi using the Monte Carlo method",
        )
        mb.def_function[generate_samples](
            "generate_samples",
            docstring="Generate Monte Carlo samples and return coordinates and results",
        )
        return mb.finalize()
    except e:
        abort(String("error creating Python Mojo module:", e))


def estimate_pi(py_samples: PythonObject) raises -> PythonObject:
    """Estimate pi using Monte Carlo method.

    Args:
        py_samples: Number of random samples to generate.

    Returns:
        Estimated value of pi.
    """
    var samples = Int(py=py_samples)
    var inside_circle: Int = 0

    for _ in range(samples):
        var x = random_float64()
        var y = random_float64()
        var distance = sqrt(x * x + y * y)

        if distance <= 1.0:
            inside_circle += 1

    # pi ~= 4 * (points inside circle / total points)
    var pi_estimate = 4.0 * Float64(inside_circle) / Float64(samples)
    return PythonObject(pi_estimate)


def generate_samples(py_samples: PythonObject) raises -> PythonObject:
    """Generate Monte Carlo samples and return coordinates and results.

    Args:
        py_samples: Number of random samples to generate.

    Returns:
        Dictionary with 'x', 'y', 'inside' arrays and 'pi_estimate',
        'error', and 'samples' entries.
    """
    var samples = Int(py=py_samples)

    # Allocate Python lists for results
    var x_coords = Python.list()
    var y_coords = Python.list()
    var inside_flags = Python.list()
    var inside_circle: Int = 0

    for _ in range(samples):
        var x = random_float64()
        var y = random_float64()
        var distance = sqrt(x * x + y * y)
        var is_inside = distance <= 1.0

        _ = x_coords.append(x)
        _ = y_coords.append(y)
        _ = inside_flags.append(is_inside)

        if is_inside:
            inside_circle += 1

    var pi_estimate = 4.0 * Float64(inside_circle) / Float64(samples)
    var pi_actual = 3.14159265358979323846
    var error = abs(pi_estimate - pi_actual)

    # Return dictionary
    var result = Python.dict()
    result["x"] = x_coords
    result["y"] = y_coords
    result["inside"] = inside_flags
    result["pi_estimate"] = PythonObject(pi_estimate)
    result["error"] = PythonObject(error)
    result["samples"] = PythonObject(samples)

    return result
