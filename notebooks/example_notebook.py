import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    dir(mo)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    """)
    return


if __name__ == "__main__":
    app.run()
