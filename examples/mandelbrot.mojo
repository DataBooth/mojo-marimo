"""
Mandelbrot Set Calculation
Computes iteration counts for points in the complex plane to visualize the Mandelbrot set.
"""

fn mandelbrot_point(cx: Float64, cy: Float64, max_iter: Int) -> Int:
    """Calculate iterations for a single point in the Mandelbrot set.
    
    Args:
        cx: Real component of complex number c.
        cy: Imaginary component of complex number c.
        max_iter: Maximum number of iterations.
    
    Returns:
        Number of iterations before divergence (or max_iter if bounded).
    """
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

fn compute_mandelbrot(width: Int, height: Int, max_iter: Int, 
                       x_min: Float64, x_max: Float64,
                       y_min: Float64, y_max: Float64) -> None:
    """Compute the Mandelbrot set for a grid of points.
    
    Args:
        width: Number of points in x direction.
        height: Number of points in y direction.
        max_iter: Maximum iterations per point.
        x_min: Minimum real axis value.
        x_max: Maximum real axis value.
        y_min: Minimum imaginary axis value.
        y_max: Maximum imaginary axis value.
    """
    var dx = (x_max - x_min) / Float64(width)
    var dy = (y_max - y_min) / Float64(height)
    
    # Compute and print iteration values as CSV
    for row in range(height):
        var cy = y_min + Float64(row) * dy
        for col in range(width):
            var cx = x_min + Float64(col) * dx
            var iterations = mandelbrot_point(cx, cy, max_iter)
            print(iterations, end="")
            if col < width - 1:
                print(",", end="")
        print()  # Newline after each row

fn main():
    # Standard Mandelbrot view
    var width = 400
    var height = 300
    var max_iter = 256
    var x_min = -2.5
    var x_max = 1.0
    var y_min = -1.25
    var y_max = 1.25
    
    compute_mandelbrot(width, height, max_iter, x_min, x_max, y_min, y_max)
