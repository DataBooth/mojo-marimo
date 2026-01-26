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
        # Monte Carlo Pi Estimation - Extension Module Pattern

        This notebook demonstrates using Mojo extension modules (`.so` files) for **zero subprocess overhead**.

        ## How it works
        1. Generate random points (x, y) in a unit square [0,1] × [0,1]
        2. Check if each point falls inside the unit circle (x² + y² ≤ 1)
        3. π ≈ 4 × (points inside circle / total points)

        **Pattern**: Import compiled `.so` module - direct function calls, no subprocess
        """
    )
    return


@app.cell
def _(mo):
    import mojo.importer  # Register import hook for auto-compilation
    import monte_carlo_ext  # Auto-compiles examples/monte_carlo_ext.mojo

    mo.md("✅ **Extension module imported** - First import compiles `.mojo` → `.so` (~1-2s)")
    return mojo, monte_carlo_ext


@app.cell
def _(mo):
    samples_slider = mo.ui.slider(
        start=1000,
        stop=10_000_000,
        step=10000,
        value=100_000,
        label="Number of samples",
        show_value=True,
    )
    samples_slider
    return (samples_slider,)


@app.cell
def _(mo, monte_carlo_ext, samples_slider):
    import math

    # Direct function call - zero subprocess overhead!
    pi_estimate = monte_carlo_ext.estimate_pi(samples_slider.value)
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
        
        **Call overhead**: ~0.01-0.1ms (direct function call, no subprocess)
        """
    )
    return error, error_percent, math, pi_actual, pi_estimate


@app.cell
def _(mo):
    mo.md(
        """
        ## Visualize Sample Points
        
        Generate a smaller sample set and visualize the points:
        """
    )
    return


@app.cell
def _(mo, monte_carlo_ext):
    import plotly.graph_objects as go

    # Generate samples with coordinates
    viz_samples = 5000
    result_dict = monte_carlo_ext.generate_samples(viz_samples)

    # Extract data
    x_coords = result_dict["x"]
    y_coords = result_dict["y"]
    inside_flags = result_dict["inside"]
    pi_est = result_dict["pi_estimate"]

    # Separate inside/outside points
    x_inside = [x for x, inside in zip(x_coords, inside_flags) if inside]
    y_inside = [y for y, inside in zip(y_coords, inside_flags) if inside]
    x_outside = [x for x, inside in zip(x_coords, inside_flags) if not inside]
    y_outside = [y for y, inside in zip(y_coords, inside_flags) if not inside]

    # Create scatter plot
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x_inside,
            y=y_inside,
            mode="markers",
            name="Inside circle",
            marker=dict(color="#06d6a0", size=3, opacity=0.6),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_outside,
            y=y_outside,
            mode="markers",
            name="Outside circle",
            marker=dict(color="#ef476f", size=3, opacity=0.6),
        )
    )

    # Add unit circle
    import numpy as np

    theta = np.linspace(0, 2 * np.pi, 100)
    fig.add_trace(
        go.Scatter(
            x=np.cos(theta),
            y=np.sin(theta),
            mode="lines",
            name="Unit circle",
            line=dict(color="black", width=2, dash="dash"),
        )
    )

    fig.update_layout(
        title=f"Monte Carlo Simulation ({viz_samples:,} samples, π ≈ {pi_est:.4f})",
        xaxis_title="x",
        yaxis_title="y",
        width=600,
        height=600,
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1]),
        yaxis_scaleanchor="x",
    )

    scatter_plot = mo.ui.plotly(fig)
    scatter_plot
    return (
        fig,
        go,
        inside_flags,
        np,
        pi_est,
        result_dict,
        scatter_plot,
        theta,
        viz_samples,
        x_coords,
        x_inside,
        x_outside,
        y_coords,
        y_inside,
        y_outside,
    )


@app.cell
def _(mo):
    mo.md(
        """
        ## Convergence Analysis
        
        Test performance across different sample sizes:
        """
    )
    return


@app.cell
def _(go, mo, monte_carlo_ext):
    import math

    # Test different sample sizes
    sample_sizes = [10**i for i in range(2, 7)]
    estimates = []
    errors = []

    for n in sample_sizes:
        est = monte_carlo_ext.estimate_pi(n)
        estimates.append(est)
        errors.append(abs(est - math.pi))

    # Convergence plot
    fig_conv = go.Figure()
    fig_conv.add_trace(
        go.Scatter(
            x=sample_sizes,
            y=estimates,
            mode="lines+markers",
            name="Mojo Estimate",
            line=dict(color="#ff6b35", width=3),
            marker=dict(size=10),
        )
    )
    fig_conv.add_hline(y=math.pi, line_dash="dash", line_color="green", annotation_text="Actual π")
    fig_conv.update_layout(
        title="Monte Carlo Convergence to π (Extension Module)",
        xaxis_title="Number of Samples",
        yaxis_title="Estimated π",
        xaxis_type="log",
        height=400,
    )

    mo.ui.plotly(fig_conv)
    return errors, est, estimates, fig_conv, n, sample_sizes


@app.cell
def _(errors, go, mo, sample_sizes):
    # Error plot
    fig_error = go.Figure()
    fig_error.add_trace(
        go.Scatter(
            x=sample_sizes,
            y=errors,
            mode="lines+markers",
            name="Absolute Error",
            line=dict(color="#d62828", width=3),
            marker=dict(size=10),
        )
    )
    fig_error.update_layout(
        title="Estimation Error vs Sample Size",
        xaxis_title="Number of Samples",
        yaxis_title="Absolute Error",
        xaxis_type="log",
        yaxis_type="log",
        height=400,
    )
    mo.ui.plotly(fig_error)
    return (fig_error,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Pattern Summary
        
        **Extension Module Pattern**:
        - ✅ **Zero subprocess overhead** (~0.01-0.1ms per call)
        - ✅ **1000× faster** than decorator/executor patterns
        - ✅ Auto-compilation via `mojo.importer`
        - ⚠️ More complex Mojo code (requires `PythonModuleBuilder`)
        - ⚠️ Best for tight loops or production systems
        
        **Performance**: 
        - First import: ~1-2s (compile .mojo → .so)
        - Subsequent calls: ~0.01-0.1ms (direct function call)
        - Recompiles automatically when source changes
        """
    )
    return


if __name__ == "__main__":
    app.run()
