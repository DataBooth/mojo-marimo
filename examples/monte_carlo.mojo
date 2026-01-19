"""
Monte Carlo Pi Estimation
Estimates π by randomly sampling points in a unit square and checking if they fall inside a unit circle.
"""

from random import random_float64
from math import sqrt

fn estimate_pi(samples: Int) -> Float64:
    """Estimate π using Monte Carlo method."""
    var inside_circle: Int = 0
    
    for _ in range(samples):
        var x = random_float64()
        var y = random_float64()
        var distance = sqrt(x * x + y * y)
        
        if distance <= 1.0:
            inside_circle += 1
    
    # π ≈ 4 * (points inside circle / total points)
    return 4.0 * Float64(inside_circle) / Float64(samples)

fn main():
    var samples = 1_000_000
    var pi_estimate = estimate_pi(samples)
    var pi_actual = 3.14159265358979323846
    var error = abs(pi_estimate - pi_actual)
    
    print("Monte Carlo Pi Estimation")
    print("Samples:", samples)
    print("Estimate:", pi_estimate)
    print("Actual π:", pi_actual)
    print("Error:", error)
