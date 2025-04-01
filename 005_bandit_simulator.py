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
def _(Bandit, arms_probs, np, px):
    probs = [float(p) for p in arms_probs.value.split(",")]

    n_arms = len(probs)
    bandit = Bandit(n_arms)

    x = np.linspace(0, 1.0, 100)

    for i in range(100):
        arm = bandit.pull()
        reward = np.random.random() < probs[arm]
        bandit.update(arm, reward)

    for arm in range(n_arms):
        success, failure = bandit.engagements[arm] + 1
        impressions = bandit.impressions[arm] + 1
        print(
            f"Arm {arm} (prob={probs[arm]}) has a success rate of {success / impressions} ({int(success)} / {int(failure)})"
        )


    fig = px.line(
        x=x,
        y=[bandit.beta_pdf(x, arm) for arm in range(n_arms)],
        title="Arm distribution",
        # labels=[] doesn't work
    )
    for arm in range(n_arms):
        fig.data[arm].name = f"arm {arm + 1}"

    fig
    return (
        arm,
        bandit,
        failure,
        fig,
        i,
        impressions,
        n_arms,
        probs,
        reward,
        success,
        x,
    )


if __name__ == "__main__":
    app.run()
