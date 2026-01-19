"""
Mandelbrot Set Calculation - Python Extension Module
Provides zero-overhead Python callable functions using PythonModuleBuilder.
"""

from python.python import PythonModuleBuilder, PythonObject

fn mandelbrot_point(cx: Float64, cy: Float64, max_iter: Int) -> Int:
    """Calculate iterations for a single point in the Mandelbrot set."""
    var x: Float64 = 0.0
    var y: Float64 = 0.0
    var iteration: Int = 0
    
    while x * x + y * y <= 4.0 and iteration < max_iter:
        let x_new = x * x - y * y + cx
        let y_new = 2.0 * x * y + cy
        x = x_new
        y = y_new
        iteration += 1
    
    return iteration

fn compute_mandelbrot(py_width: PythonObject, py_height: PythonObject, 
                      py_max_iter: PythonObject,
                      py_x_min: PythonObject, py_x_max: PythonObject,
                      py_y_min: PythonObject, py_y_max: PythonObject) raises -> PythonObject:
    """Compute the Mandelbrot set and return as nested list (2D array).
    
    Args:
        py_width: Number of points in x direction.
        py_height: Number of points in y direction.
        py_max_iter: Maximum iterations per point.
        py_x_min: Minimum real axis value.
        py_x_max: Maximum real axis value.
        py_y_min: Minimum imaginary axis value.
        py_y_max: Maximum imaginary axis value.
    
    Returns:
        2D list of iteration counts (height x width).
    """
    var width = Int(py_width)
    var height = Int(py_height)
    var max_iter = Int(py_max_iter)
    var x_min = Float64(py_x_min)
    var x_max = Float64(py_x_max)
    var y_min = Float64(py_y_min)
    var y_max = Float64(py_y_max)
    
    var dx = (x_max - x_min) / Float64(width)
    var dy = (y_max - y_min) / Float64(height)
    
    # Build result as nested Python list
    var result = PythonObject([])
    
    for row in range(height):
        var cy = y_min + Float64(row) * dy
        var row_data = PythonObject([])
        
        for col in range(width):
            var cx = x_min + Float64(col) * dx
            var iterations = mandelbrot_point(cx, cy, max_iter)
            _ = row_data.append(iterations)
        
        _ = result.append(row_data)
    
    return result

fn initialize(module: PythonModuleBuilder) -> None:
    """Initialize the Python module with exported functions."""
    module.add_function("compute_mandelbrot", compute_mandelbrot)
