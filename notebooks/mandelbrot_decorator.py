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
        # Mandelbrot Set - Decorator Pattern

        Visualize the beautiful Mandelbrot fractal using Mojo's performance with the decorator pattern.

        ## The Mandelbrot Set
        For each point c in the complex plane, iterate: z_(n+1) = z_n² + c  
        Starting with z_0 = 0, count iterations until |z| > 2 (diverges) or max iterations reached.

        **Pattern**: Mojo code in docstring, called like Python function
        """
    )
    return


@app.cell
def _(mo):
    from mojo_marimo import mojo
    import numpy as np
    
    @mojo
    def compute_mandelbrot(width: int, height: int, max_iter: int) -> str:
        """
        fn mandelbrot_point(cx: Float64, cy: Float64, max_iter: Int) -> Int:
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

        fn main():
            var width = {{width}}
            var height = {{height}}
            var max_iter = {{max_iter}}
            var x_min = -2.5
            var x_max = 1.0
            var y_min = -1.25
            var y_max = 1.25
            var dx = (x_max - x_min) / Float64(width)
            var dy = (y_max - y_min) / Float64(height)
            
            for row in range(height):
                var cy = y_min + Float64(row) * dy
                for col in range(width):
                    var cx = x_min + Float64(col) * dx
                    var iterations = mandelbrot_point(cx, cy, max_iter)
                    print(iterations, end="")
                    if col < width - 1:
                        print(",", end="")
                print()
        """
        ...
    
    mo.md("✅ **Mojo Mandelbrot function defined**")
    return compute_mandelbrot, np


@app.cell
def _(mo):
    # UI controls
    width_slider = mo.ui.slider(50, 800, value=400, step=50, label="Width", show_value=True)
    height_slider = mo.ui.slider(50, 600, value=300, step=50, label="Height", show_value=True)
    max_iter_slider = mo.ui.slider(50, 500, value=256, step=50, label="Max Iterations", show_value=True)
    
    mo.hstack([width_slider, height_slider, max_iter_slider])
    return height_slider, max_iter_slider, width_slider


@app.cell
def _(compute_mandelbrot, height_slider, max_iter_slider, mo, np, width_slider):
    # Compute Mandelbrot set
    result = compute_mandelbrot(width_slider.value, height_slider.value, max_iter_slider.value)
    
    # Parse CSV output into 2D array
    lines = result.split('\n')
    data = []
    for line in lines:
        if line.strip() and ',' in line:
            row = [int(x) for x in line.split(',')]
            data.append(row)
    
    mandelbrot_array = np.array(data)
    
    mo.md(f"✅ **Computed {width_slider.value}×{height_slider.value} grid** ({mandelbrot_array.size:,} points)")
    return data, line, lines, mandelbrot_array, result, row, x


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
        ## Pattern Summary
        
        **Decorator Pattern (`@mojo`)**:
        - ✅ Clean, Pythonic API
        - ✅ Self-documenting (Mojo code visible in docstring)
        - ✅ Template parameters with `{{param}}` syntax
        - ⚠️ Subprocess overhead (~10-50ms per call after caching)
        
        **Performance**: First call ~1-2s (compile), subsequent ~10-50ms (cached binary)
        
        The Mandelbrot set showcases Mojo's floating-point performance and tight loops.
        """
    )
    return


if __name__ == "__main__":
    app.run()
