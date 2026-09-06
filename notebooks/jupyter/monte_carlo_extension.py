# %% [markdown]
# # Monte Carlo π Estimation - Extension Module Pattern 🔥
#
# Uses compiled Mojo extension module (`.so`) for zero-overhead FFI calls.
#
# **Performance**: ~1000× faster function calls than subprocess patterns (no overhead, direct FFI).

# %%
import sys
from pathlib import Path

# The .mojo source lives in examples/ (two levels up from this notebook)
examples_dir = Path(__file__).parent.parent.parent / "examples"
sys.path.insert(0, str(examples_dir))

# Register the Mojo import hook (compiles .mojo → .so on demand)
import mojo.importer

# Import the Mojo extension module
import monte_carlo_ext

# %%
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# %% [markdown]
# ## Monte Carlo Method
#
# Estimates π by randomly sampling points in a unit square and checking if they fall within a unit circle:
#
# - Generate random (x, y) coordinates in [0, 1]
# - Check if x² + y² ≤ 1 (inside circle)
# - π ≈ 4 × (points inside circle) / (total points)

# %% [markdown]
# ## Small Sample (10,000 points)

# %%
# Generate samples - returns a dict with 'x', 'y', 'inside', 'pi_estimate', 'error'
res_small = monte_carlo_ext.generate_samples(10_000)
x_small = np.array(res_small["x"])
y_small = np.array(res_small["y"])
inside_small = np.array(res_small["inside"], dtype=int)
pi_small = res_small["pi_estimate"]
error_small = res_small["error"]

print("Samples: 10,000")
print(f"π estimate: {pi_small:.6f}")
print(f"Error: {abs(pi_small - np.pi):.6f}")
print(f"Inside circle: {inside_small.sum():,} points")

# %% [markdown]
# ## Visualise Small Sample

# %%
# Convert numpy arrays for plotting
x_inside = x_small[inside_small == 1]
y_inside = y_small[inside_small == 1]
x_outside = x_small[inside_small == 0]
y_outside = y_small[inside_small == 0]

fig = go.Figure()

# Points inside circle
fig.add_trace(
    go.Scatter(
        x=x_inside,
        y=y_inside,
        mode="markers",
        marker=dict(size=3, color="blue", opacity=0.6),
        name="Inside circle",
    )
)

# Points outside circle
fig.add_trace(
    go.Scatter(
        x=x_outside,
        y=y_outside,
        mode="markers",
        marker=dict(size=3, color="red", opacity=0.6),
        name="Outside circle",
    )
)

fig.update_layout(
    title=f"Monte Carlo π Estimation (10K points)<br>π ≈ {pi_small:.6f}",
    xaxis_title="x",
    yaxis_title="y",
    width=600,
    height=600,
    showlegend=True,
)

fig.show()

# %% [markdown]
# ## Large Sample (1,000,000 points)

# %%
# Generate large sample
res_large = monte_carlo_ext.generate_samples(1_000_000)
x_large = np.array(res_large["x"])
y_large = np.array(res_large["y"])
inside_large = np.array(res_large["inside"], dtype=int)
pi_large = res_large["pi_estimate"]
error_large = res_large["error"]

print("Samples: 1,000,000")
print(f"π estimate: {pi_large:.6f}")
print(f"Error: {abs(pi_large - np.pi):.6f}")
print(f"Actual π: {np.pi:.6f}")

# %% [markdown]
# ## Convergence Analysis

# %%
# Test different sample sizes
sample_sizes = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
estimates = []
errors = []

for n in sample_sizes:
    pi_est = monte_carlo_ext.generate_samples(n)["pi_estimate"]
    estimates.append(pi_est)
    errors.append(abs(pi_est - np.pi))

# Plot convergence
fig = make_subplots(
    rows=1, cols=2, subplot_titles=("π Estimate vs Sample Size", "Absolute Error vs Sample Size")
)

# Estimates
fig.add_trace(
    go.Scatter(x=sample_sizes, y=estimates, mode="lines+markers", name="Estimate"), row=1, col=1
)
fig.add_hline(y=np.pi, line_dash="dash", line_color="red", row=1, col=1)

# Errors
fig.add_trace(
    go.Scatter(
        x=sample_sizes, y=errors, mode="lines+markers", name="Error", line=dict(color="red")
    ),
    row=1,
    col=2,
)

fig.update_xaxes(title_text="Sample Size", type="log", row=1, col=1)
fig.update_xaxes(title_text="Sample Size", type="log", row=1, col=2)
fig.update_yaxes(title_text="π Estimate", row=1, col=1)
fig.update_yaxes(title_text="Absolute Error", type="log", row=1, col=2)

fig.update_layout(height=400, showlegend=False, title_text="Monte Carlo Convergence")
fig.show()

# %% [markdown]
# ## Extension Module Performance
#
# **Key Advantage**: Direct FFI calls to Mojo code with NO subprocess overhead.
#
# - **Decorator/Executor patterns**: ~10-50ms per call (subprocess overhead)
# - **Extension module**: ~0.01ms per call (~1000× faster)
#
# **Trade-off**: More complex Mojo code (requires `PythonModuleBuilder`), but worth it for frequently called functions.
#
# See `examples/monte_carlo_ext.mojo` for the extension module implementation.
