import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from lib.bandit import Bandit
    import plotly.express as px
    import math
    import polars as pl
    return Bandit, math, mo, np, pl, px


@app.cell
def _(mo):
    mo.md("""# Multi-Armed Bandit Simulator""")
    return


@app.cell
def _(mo):
    arms_probs = mo.ui.text(label="Arm probabilities", value="0.7,0.3,0.1")
    arms_probs
    return (arms_probs,)


@app.cell
def _(Bandit, arms_probs, np):
    probs = [float(p) for p in arms_probs.value.split(",")]

    n_arms = len(probs)
    bandit = Bandit(n_arms)

    x = np.linspace(0, 1.0, 100)
    data = []

    for i in range(100):
        arm = bandit.pull()
        reward = np.random.random() < probs[arm]
        bandit.update(arm, reward)

        for ai in range(n_arms):
            y = bandit.beta_pdf(x, ai)
            for xi, yi in zip(x, y):
                data.append((i, ai, xi, yi))

    for arm in range(n_arms):
        success, failure = bandit.engagements[arm] + 1
        impressions = bandit.impressions[arm] + 1
        print(
            f"Arm {arm} (prob={probs[arm]}) has a success rate of {success / impressions} ({int(success)} / {int(failure)})"
        )
    return (
        ai,
        arm,
        bandit,
        data,
        failure,
        i,
        impressions,
        n_arms,
        probs,
        reward,
        success,
        x,
        xi,
        y,
        yi,
    )


@app.cell
def _(data, pl):
    df = pl.from_records(
        [dict(i=i, arm=arm, x=xi, y=yi) for (i, arm, xi, yi) in data]
    )
    return (df,)


@app.cell
def _(df, px):
    fig = px.line(
        df,
        x="x",
        y="y",
        color="arm",
        animation_group="arm",
        animation_frame="i",
        range_x=[0, 1],
        range_y=[0, 10],
    )
    fig
    return (fig,)


if __name__ == "__main__":
    app.run()
