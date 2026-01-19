import marimo

__generated_with = "0.10.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # Monte Carlo Pi Estimation - Executor Pattern

        This notebook demonstrates using `run_mojo()` executor to estimate π using the Monte Carlo method.

        ## How it works
        1. Generate random points (x, y) in a unit square [0,1] × [0,1]
        2. Check if each point falls inside the unit circle (x² + y² ≤ 1)
        3. π ≈ 4 × (points inside circle / total points)

        **Pattern**: Pass Mojo code as string or file path to `run_mojo()`
        """
    )
    return


@app.cell
def _(mo):
    from mojo_marimo import run_mojo
    from pathlib import Path
    
    # Path to standalone Mojo file
    mojo_file = Path("examples/monte_carlo.mojo")
    
    mo.md(f"✅ **Using Mojo file**: `{mojo_file}`")
    return Path, mojo_file, run_mojo


@app.cell
def _(mo):
    samples_slider = mo.ui.slider(
        start=1000,
        stop=10_000_000,
        step=10000,
        value=100_000,
        label="Number of samples",
        show_value=True
    )
    samples_slider
    return (samples_slider,)


@app.cell
def _(mo, samples_slider):
    # Build dynamic Mojo code
    mojo_code = f"""
from random import random_float64
from math import sqrt

fn estimate_pi(samples: Int) -> Float64:
    var inside_circle: Int = 0
    
    for _ in range(samples):
        var x = random_float64()
        var y = random_float64()
        var distance = sqrt(x * x + y * y)
        
        if distance <= 1.0:
            inside_circle += 1
    
    return 4.0 * Float64(inside_circle) / Float64(samples)

fn main():
    var pi_estimate = estimate_pi({samples_slider.value})
    print(pi_estimate)
"""
    
    mo.md("✅ **Dynamic Mojo code generated**")
    return (mojo_code,)


@app.cell
def _(mojo_code, mo, run_mojo, samples_slider):
    import math
    
    # Execute Mojo code
    result = run_mojo(mojo_code)
    
    if result is None:
        mo.md("❌ **Compilation or execution failed**")
    else:
        pi_estimate = float(result.strip())
        pi_actual = math.pi
        error = abs(pi_estimate - pi_actual)
        error_percent = (error / pi_actual) * 100
        
        mo.md(
            f"""
            ## Results
            
            **Samples**: {samples_slider.value:,}  
            **Estimated π**: {pi_estimate:.10f}  
            **Actual π**: {pi_actual:.10f}  
            **Error**: {error:.10f} ({error_percent:.4f}%)
            """
        )
    return error, error_percent, math, pi_actual, pi_estimate, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Convergence Visualization
        
        Generate estimates for different sample sizes:
        """
    )
    return


@app.cell
def _(mo, run_mojo):
    import plotly.graph_objects as go
    import math
    
    # Generate estimates for different sample sizes
    sample_sizes = [10**i for i in range(2, 7)]
    estimates = []
    errors = []
    
    for n in sample_sizes:
        code = f"""
from random import random_float64
from math import sqrt

fn estimate_pi(samples: Int) -> Float64:
    var inside_circle: Int = 0
    for _ in range(samples):
        var x = random_float64()
        var y = random_float64()
        if sqrt(x * x + y * y) <= 1.0:
            inside_circle += 1
    return 4.0 * Float64(inside_circle) / Float64(samples)

fn main():
    print(estimate_pi({n}))
"""
        result = run_mojo(code)
        if result:
            est = float(result.strip())
            estimates.append(est)
            errors.append(abs(est - math.pi))
    
    # Convergence plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sample_sizes, y=estimates,
        mode='lines+markers', name='Mojo Estimate',
        line=dict(color='#ff6b35', width=3), marker=dict(size=10)
    ))
    fig.add_hline(y=math.pi, line_dash="dash", line_color="green", annotation_text="Actual π")
    fig.update_layout(
        title="Monte Carlo Convergence to π",
        xaxis_title="Number of Samples", yaxis_title="Estimated π",
        xaxis_type="log", height=400
    )
    
    mo.ui.plotly(fig)
    return code, errors, est, estimates, fig, go, n, sample_sizes


@app.cell
def _(errors, go, mo, sample_sizes):
    # Error plot
    fig_error = go.Figure()
    fig_error.add_trace(go.Scatter(
        x=sample_sizes, y=errors,
        mode='lines+markers', name='Absolute Error',
        line=dict(color='#d62828', width=3), marker=dict(size=10)
    ))
    fig_error.update_layout(
        title="Estimation Error vs Sample Size",
        xaxis_title="Number of Samples", yaxis_title="Absolute Error",
        xaxis_type="log", yaxis_type="log", height=400
    )
    mo.ui.plotly(fig_error)
    return (fig_error,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Pattern Summary
        
        **Executor Pattern (`run_mojo()`)**:
        - ✅ Dynamic code generation (templates, algorithms)
        - ✅ Can execute .mojo files or inline code
        - ✅ Explicit control over execution
        - ⚠️ Subprocess overhead (~10-50ms per call after caching)
        
        **Performance**: First call ~1-2s (compile), subsequent ~10-50ms (cached binary)
        """
    )
    return


if __name__ == "__main__":
    app.run()
