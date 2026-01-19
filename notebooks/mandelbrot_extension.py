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
        # Mandelbrot Set - Extension Module Pattern

        Visualize the Mandelbrot fractal using Mojo extension modules for **zero subprocess overhead**.

        ## The Mandelbrot Set
        For each point c in the complex plane, iterate: z_(n+1) = z_n² + c  
        Starting with z_0 = 0, count iterations until |z| > 2 (diverges) or max iterations reached.

        **Pattern**: Import compiled `.so` module - direct function calls
        """
    )
    return


@app.cell
def _(mo):
    import mojo.importer  # Register import hook
    import mandelbrot_ext  # Auto-compiles examples/mandelbrot_ext.mojo
    import numpy as np
    
    mo.md("✅ **Extension module imported** - First import compiles `.mojo` → `.so` (~1-2s)")
    return mandelbrot_ext, mojo, np


@app.cell
def _(mo):
    # UI controls
    width_slider = mo.ui.slider(50, 800, value=400, step=50, label="Width", show_value=True)
    height_slider = mo.ui.slider(50, 600, value=300, step=50, label="Height", show_value=True)
    max_iter_slider = mo.ui.slider(50, 500, value=256, step=50, label="Max Iterations", show_value=True)
    
    mo.hstack([width_slider, height_slider, max_iter_slider])
    return height_slider, max_iter_slider, width_slider


@app.cell
def _(height_slider, mandelbrot_ext, max_iter_slider, mo, np, width_slider):
    # Direct function call - zero subprocess overhead!
    result_list = mandelbrot_ext.compute_mandelbrot(
        width_slider.value, 
        height_slider.value, 
        max_iter_slider.value,
        -2.5, 1.0,  # x_min, x_max
        -1.25, 1.25  # y_min, y_max
    )
    
    # Convert to numpy array
    mandelbrot_array = np.array(result_list)
    
    mo.md(f"✅ **Computed {width_slider.value}×{height_slider.value} grid** ({mandelbrot_array.size:,} points)")
    return mandelbrot_array, result_list


@app.cell
def _(height_slider, mandelbrot_array, max_iter_slider, mo, width_slider):
    import plotly.graph_objects as go
    
    fig = go.Figure(data=go.Heatmap(
        z=mandelbrot_array,
        colorscale='Hot',
        colorbar=dict(title="Iterations"),
        hovertemplate='x: %{x}<br>y: %{y}<br>iterations: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Mandelbrot Set ({width_slider.value}×{height_slider.value}, max_iter={max_iter_slider.value})",
        xaxis_title="Real axis",
        yaxis_title="Imaginary axis",
        width=800,
        height=600,
        yaxis=dict(scaleanchor="x")
    )
    
    mandelbrot_plot = mo.ui.plotly(fig)
    mandelbrot_plot
    return fig, go, mandelbrot_plot


@app.cell
def _(mo):
    mo.md(
        """
        ## Zoom Into Details
        
        Explore different regions of the Mandelbrot set:
        """
    )
    return


@app.cell
def _(mo):
    # Region selector
    region = mo.ui.dropdown(
        options={
            "Full view": (-2.5, 1.0, -1.25, 1.25),
            "Main body": (-0.8, -0.4, -0.2, 0.2),
            "Spiral": (-0.7, -0.65, 0.35, 0.4),
            "Seahorse valley": (-0.75, -0.735, 0.095, 0.11),
        },
        value="Full view",
        label="Region"
    )
    region
    return (region,)


@app.cell
def _(mandelbrot_ext, mo, np, region):
    import plotly.graph_objects as go
    
    # Get region bounds
    x_min, x_max, y_min, y_max = region.value
    
    # Compute zoomed region
    zoom_data = mandelbrot_ext.compute_mandelbrot(
        500, 400, 512,
        x_min, x_max, y_min, y_max
    )
    zoom_array = np.array(zoom_data)
    
    fig_zoom = go.Figure(data=go.Heatmap(
        z=zoom_array,
        colorscale='Hot',
        colorbar=dict(title="Iterations")
    ))
    
    fig_zoom.update_layout(
        title=f"Mandelbrot Set - {region.value}",
        xaxis_title="Real axis",
        yaxis_title="Imaginary axis",
        width=800,
        height=640,
        yaxis=dict(scaleanchor="x")
    )
    
    mo.ui.plotly(fig_zoom)
    return fig_zoom, go, x_max, x_min, y_max, y_min, zoom_array, zoom_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Pattern Summary
        
        **Extension Module Pattern**:
        - ✅ **Zero subprocess overhead** (~0.01-0.1ms per call)
        - ✅ **1000× faster** than decorator/executor patterns
        - ✅ Auto-compilation via `mojo.importer`
        - ✅ Perfect for interactive exploration (slider responsiveness)
        - ⚠️ More complex Mojo code (requires `PythonModuleBuilder`)
        
        **Performance**: 
        - First import: ~1-2s (compile .mojo → .so)
        - Subsequent calls: ~0.01-0.1ms (direct function call)
        - Ideal for computationally intensive visualizations
        
        The Mandelbrot set showcases Mojo's floating-point performance in tight loops.
        """
    )
    return


if __name__ == "__main__":
    app.run()
