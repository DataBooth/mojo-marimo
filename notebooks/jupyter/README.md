# Jupyter Notebooks

Jupyter-native versions of `mojo-marimo` examples. These are standard Python files with `# %%` cell markers that work in:

- **Jupyter Notebook** / JupyterLab
- **VSCode** (Python Interactive Window)
- **PyCharm** (Jupyter notebook support)
- **Google Colab** (upload and run)
- Any IDE with Jupyter support

## Running the Notebooks

### Option 1: Jupyter Notebook
```bash
just jupyter                    # Browse all notebooks
just jupyter-decorator          # Pattern 1: Decorator
just jupyter-executor           # Pattern 2: Executor  
just jupyter-mc                 # Monte Carlo example
```

### Option 2: Direct Command
```bash
uv run jupyter notebook notebooks/jupyter/
```

### Option 3: VSCode
1. Open any `.py` file in this directory
2. VSCode will recognise the `# %%` markers
3. Click "Run Cell" or use the interactive window

## Available Notebooks

### Pattern Examples
- **`pattern_decorator.py`** - Clean `@mojo` decorator pattern with template parameters
- **`pattern_executor.py`** - Dynamic `run_mojo()` execution with validation examples

### Interactive Examples
- **`monte_carlo_extension.py`** - Monte Carlo π estimation with visualisation
  - Uses extension module pattern (`.so` compilation)
  - Includes convergence analysis and scatter plots
  - Demonstrates ~1000× faster calls vs subprocess

## Differences from marimo Versions

These notebooks:
- ✅ Use standard `print()` instead of `mo.md()`
- ✅ Use `# %% [markdown]` for markdown cells
- ✅ Have no marimo dependencies
- ✅ Work in any Jupyter-compatible environment
- ✅ Can be converted to `.ipynb` format if needed

The marimo versions (in `notebooks/*.py`) have reactive UI elements and are designed for the marimo notebook system.

## Converting to .ipynb

The `.ipynb` files are already included in this directory. To regenerate them:

```bash
# Convert all .py files to .ipynb
just jupyter-convert

# Or convert individual files
uv run jupytext --to notebook pattern_decorator.py
```

VSCode can also open `.py` files directly with the interactive window, or use "Export as Jupyter Notebook".
