import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from lib.ab import sample_size_for_proportions
    return mo, sample_size_for_proportions


@app.cell
def _(mo):
    mo.md("""# A/B Test Calculator""")
    return


@app.cell
def _(mo):
    conversion_control = mo.ui.number(
        start=0,
        stop=100,
        step=0.01,
        value=2,
        label="Conversion rate control (in %)",
    )
    uplift = mo.ui.number(value=15, label="Expected uplift (in %)")

    hypothesis = mo.ui.radio(
        options={"one-sided": "smaller", "two-sided": "two-sided"},
        value="two-sided",
        label="Hypothesis",
    )

    beta = mo.ui.radio(
        options={"75%": 0.75, "80%": 0.80, "90%": 0.9, "95%": 0.95},
        value="80%",
        label="Power (beta)",
    )

    confidence = mo.ui.radio(
        options={"90%": 0.9, "95%": 0.95, "99%": 0.99},
        value="95%",
        label="Confidence (1 - alpha)",
    )


    mo.vstack([conversion_control, uplift, confidence, beta, hypothesis])
    return beta, confidence, conversion_control, hypothesis, uplift


@app.cell
def _(
    beta,
    confidence,
    conversion_control,
    hypothesis,
    mo,
    sample_size_for_proportions,
    uplift,
):
    p1 = conversion_control.value / 100
    p2 = float((uplift.value + 100) / 100.0 * p1)

    alternative = hypothesis.value
    alpha = 1 - confidence.value
    power = beta.value

    sample_size = sample_size_for_proportions(
        p1, p2, alpha=alpha, power=power, alternative=alternative
    )
    mo.md(
        f"## Sample size of **{sample_size:,}** is required to achieve a conversion rate of {p2:0.2%}"
    )
    return alpha, alternative, p1, p2, power, sample_size


if __name__ == "__main__":
    app.run()
