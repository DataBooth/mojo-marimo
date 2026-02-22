# %% [markdown]
# # Monte Carlo Pi Estimation - Executor Pattern
#
# This notebook demonstrates using `run_mojo()` executor to estimate π using the Monte Carlo method.
#
# ## How it works
# 1. Generate random points (x, y) in a unit square [0,1] × [0,1]
# 2. Check if each point falls inside the unit circle (x² + y² ≤ 1)
# 3. π ≈ 4 × (points inside circle / total points)
#
# **Pattern**: Pass Mojo code as string or file path to `run_mojo()`

# %% [markdown]
# ## Import and setup

# %%
from pathlib import Path
from py_run_mojo.executor import run_mojo

# Path to standalone Mojo file
mojo_file = Path("examples/monte_carlo.mojo")

print(f"✅ **Using Mojo file**: `{mojo_file}`")

# %% [markdown]
# ## Test with file-based execution
#
# The standalone Mojo script in `examples/monte_carlo.mojo` prints a small report.
# It is a useful smoke test, but it does not currently accept a sample-size parameter.

# %%
file_output = run_mojo(str(mojo_file))

if file_output is None:
    raise RuntimeError("File-based compilation or execution failed")

print(file_output)

# %% [markdown]
# ## Test with inline code execution


# %%
def estimate_pi_inline(samples: int) -> float:
    """Generate and run inline Mojo code to estimate π"""

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
    var pi_estimate = estimate_pi({samples})
    print(pi_estimate)
"""

    result = run_mojo(mojo_code)

    if result is None:
        raise RuntimeError("Compilation or execution failed")

    return float(result.strip())


# Test inline execution
for samples in [1000, 10000, 100000]:
    try:
        pi_estimate = estimate_pi_inline(samples)
        error = abs(pi_estimate - math.pi)
        error_percent = (error / math.pi) * 100

        print(f"Inline execution - Samples: {samples:,}")
        print(f"Estimated π: {pi_estimate:.10f}")
        print(f"Error: {error:.10f} ({error_percent:.4f}%)")
        print("-" * 50)
    except RuntimeError as e:
        print(f"Error: {e}")

# %% [markdown]
# ## Convergence Visualisation

# %%
import numpy as np
import plotly.graph_objects as go

# Generate estimates for different sample sizes using inline execution
sample_sizes = [10**i for i in range(2, 7)]  # 100 to 1,000,000
estimates = []
errors = []

for n in sample_sizes:
    est = estimate_pi_inline(n)
    estimates.append(est)
    errors.append(abs(est - math.pi))

# Create convergence plot
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=sample_sizes,
        y=estimates,
        mode="lines+markers",
        name="Mojo Estimate",
        line=dict(color="#ff6b35", width=3),
        marker=dict(size=10),
    )
)

fig.add_hline(
    y=math.pi,
    line_dash="dash",
    line_color="green",
    annotation_text="Actual π",
    annotation_position="right",
)

fig.update_layout(
    title="Monte Carlo Convergence to π",
    xaxis_title="Number of Samples",
    yaxis_title="Estimated π",
    xaxis_type="log",
    height=400,
    hovermode="x unified",
)

fig.show()

# %% [markdown]
# ## Error Analysis

# %%
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
    hovermode="x unified",
)

fig_error.show()

# %% [markdown]
# ## Pattern Summary
#
# **Executor Pattern (`run_mojo()`)**:
# - ✅ Dynamic code generation (templates, algorithms)
# - ✅ Can execute .mojo files or inline code
# - ✅ Explicit control over execution
# - ✅ Works with standalone `.mojo` files
# - ✅ Good for existing Mojo codebases
# - ⚠️ Subprocess overhead (~10-50ms per call after caching)
# - ⚠️ File I/O overhead for file execution
#
# **Performance**: First call ~1-2s (compile), subsequent ~10-50ms (cached binary)
