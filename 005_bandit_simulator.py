import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from lib.bandit import Bandit

    plt.style.use("bmh")
    return Bandit, mo, np, plt


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
def _(Bandit, arms_probs, np, plt):
    probs = [float(p) for p in arms_probs.value.split(",")]

    n_arms = len(probs)
    bandit = Bandit(n_arms)

    x = np.linspace(0, 1.0, 100)

    for i in range(10):
        for arm in range(n_arms):
            y = bandit.beta_pdf(x, arm)
            plt.plot(x, y, label=str(probs[arm]))
        plt.legend()
        plt.title("Beta distributions for each arm (iters: %d)" % i)

        arm = bandit.pull()
        reward = np.random.random() < probs[arm]
        bandit.update(arm, reward)
        plt.show()

    for arm in range(n_arms):
        success, failure = bandit.engagements[arm] + 1
        impressions = bandit.impressions[arm] + 1
        print(
            f"Arm {arm} has a success rate of {success / impressions} ({int(success)} / {int(failure)})"
        )
    return (
        arm,
        bandit,
        failure,
        i,
        impressions,
        n_arms,
        probs,
        reward,
        success,
        x,
        y,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
