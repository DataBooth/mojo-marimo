import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Mandelbrot Set - Executor Pattern

    Visualize the Mandelbrot fractal using `run_mojo()` executor for dynamic code generation.

    ## The Mandelbrot Set
    For each point c in the complex plane, iterate: z_(n+1) = z_n² + c
    Starting with z_0 = 0, count iterations until |z| > 2 (diverges) or max iterations reached.

    **Pattern**: Pass Mojo code as string to `run_mojo()`
    """)
    return


@app.cell
def _(mo):
    import numpy as np
    from mojo_marimo import run_mojo

    mo.md("✅ **Executor imported**")
    return np, run_mojo


@app.cell
def _(mo):
    # UI controls
    width_slider = mo.ui.slider(50, 800, value=400, step=50, label="Width", show_value=True)
    height_slider = mo.ui.slider(50, 600, value=300, step=50, label="Height", show_value=True)
    max_iter_slider = mo.ui.slider(
        50, 500, value=256, step=50, label="Max Iterations", show_value=True
    )

    mo.hstack([width_slider, height_slider, max_iter_slider])
    return height_slider, max_iter_slider, width_slider


@app.cell
def _(height_slider, max_iter_slider, width_slider):
    # Build dynamic Mojo code
    mojo_code = f"""
    fn mandelbrot_point(cx: Float64, cy: Float64, max_iter: Int) -> Int:
        var x: Float64 = 0.0
        var y: Float64 = 0.0
        var iteration: Int = 0

        while x * x + y * y <= 4.0 and iteration < max_iter:
            x_new = x * x - y * y + cx
            y_new = 2.0 * x * y + cy
            x = x_new
            y = y_new
            iteration += 1
        return iteration

    fn main():
        var width = {width_slider.value}
        var height = {height_slider.value}
        var max_iter = {max_iter_slider.value}
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
    return (mojo_code,)


@app.cell
def _(mo, mojo_code):
    mo.md(f"""
    ```{mojo_code}```
    """)
    return


@app.cell
def _(mojo_code, run_mojo):
    # Execute Mojo code
    result = run_mojo(mojo_code)
    return (result,)


@app.cell
def _(height_slider, mo, np, result, width_slider):
    # Parse CSV output into 2D array
    if result is None:
        mo.md("❌ **Compilation or execution failed**")

    lines = result.split("\n")
    data = []
    for line in lines:
        if line.strip() and "," in line:
            row = [int(x) for x in line.split(",")]
            data.append(row)

    mandelbrot_array = np.array(data)

    mo.md(
        f"✅ **Computed {width_slider.value}×{height_slider.value} grid** ({mandelbrot_array.size:,} points)"
    )
    return (mandelbrot_array,)


@app.cell
def _(height_slider, mandelbrot_array, max_iter_slider, mo, width_slider):
    import plotly.graph_objects as go

    fig = go.Figure(
        data=go.Heatmap(
            z=mandelbrot_array,
            colorscale="Hot",
            colorbar=dict(title="Iterations"),
            hovertemplate="x: %{x}<br>y: %{y}<br>iterations: %{z}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Mandelbrot Set ({width_slider.value}×{height_slider.value}, max_iter={max_iter_slider.value})",
        xaxis_title="Real axis",
        yaxis_title="Imaginary axis",
        width=800,
        height=600,
        yaxis=dict(scaleanchor="x"),
    )

    mo.ui.plotly(fig)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Pattern Summary

    **Executor Pattern (`run_mojo()`)**:
    - ✅ Dynamic code generation (parameters as f-strings)
    - ✅ Can execute .mojo files or inline code
    - ✅ Explicit control over execution
    - ⚠️ Subprocess overhead (~10-50ms per call after caching)

    **Performance**: First call ~1-2s (compile), subsequent ~10-50ms (cached binary)
    """)
    return


if __name__ == "__main__":
    app.run()
