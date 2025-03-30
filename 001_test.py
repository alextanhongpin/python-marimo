import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # This is amazing

        this is cool
        """
    )
    return


@app.cell
def _():
    import math


    print(math.sqrt(10))
    return (math,)


@app.cell
def _(mo):
    x = mo.ui.slider(1, 9)
    x
    return (x,)


@app.cell
def _(x):
    print(x.value)
    return


@app.cell
def _():
    import polars as pl
    return (pl,)


@app.cell
def _(pl):
    df = pl.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df
    return (df,)


@app.cell
def _(df, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM df
        """
    )
    return


if __name__ == "__main__":
    app.run()
