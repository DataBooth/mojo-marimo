"""
Monte Carlo Pi Estimation - Python Extension Module
Provides zero-overhead Python callable functions using PythonModuleBuilder.
"""

from python.python import PythonModuleBuilder, PythonObject
from random import random_float64
from math import sqrt

fn estimate_pi(py_samples: PythonObject) raises -> PythonObject:
    """Estimate π using Monte Carlo method.
    
    Args:
        py_samples: Number of random samples to generate.
    
    Returns:
        Estimated value of π.
    """
    var samples = Int(py_samples)
    var inside_circle: Int = 0
    
    for _ in range(samples):
        var x = random_float64()
        var y = random_float64()
        var distance = sqrt(x * x + y * y)
        
        if distance <= 1.0:
            inside_circle += 1
    
    # π ≈ 4 * (points inside circle / total points)
    var pi_estimate = 4.0 * Float64(inside_circle) / Float64(samples)
    return pi_estimate

fn generate_samples(py_samples: PythonObject) raises -> PythonObject:
    """Generate Monte Carlo samples and return coordinates and results.
    
    Args:
        py_samples: Number of random samples to generate.
    
    Returns:
        Dictionary with 'x', 'y', 'inside' arrays and 'pi_estimate'.
    """
    var samples = Int(py_samples)
    
    # Allocate Python lists for results
    var x_coords = PythonObject([])
    var y_coords = PythonObject([])
    var inside_flags = PythonObject([])
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
    var result = PythonObject({})
    result["x"] = x_coords
    result["y"] = y_coords
    result["inside"] = inside_flags
    result["pi_estimate"] = pi_estimate
    result["error"] = error
    result["samples"] = samples
    
    return result

fn initialize(module: PythonModuleBuilder) -> None:
    """Initialize the Python module with exported functions."""
    module.add_function("estimate_pi", estimate_pi)
    module.add_function("generate_samples", generate_samples)
