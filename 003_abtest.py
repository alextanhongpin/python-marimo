import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import math

    import marimo as mo
    import polars as pl

    from lib.ab import (
        confint_proportions_2indep,
        power_proportions_2indep,
        test_proportions_2indep,
    )
    return (
        confint_proportions_2indep,
        math,
        mo,
        pl,
        power_proportions_2indep,
        test_proportions_2indep,
    )


@app.cell
def _(mo):
    mo.md("""# A/B Test Analysis""")
    return


@app.cell
def _(mo):
    visitors1 = mo.ui.number(value=80000, label="Visitors 1")
    conversion1 = mo.ui.number(value=1600, label="Conversion 1")
    visitors2 = mo.ui.number(value=80000, label="Visitors 2")
    conversion2 = mo.ui.number(value=1696, label="Conversion 2")

    confidence = mo.ui.radio(
        options={"90%": 0.9, "95%": 0.95, "99%": 0.99},
        value="95%",
        label="Confidence",
    )

    hypothesis = mo.ui.radio(
        options={"one-sided": "smaller", "two-sided": "two-sided"},
        value="two-sided",
        label="Hypothesis",
    )

    mo.vstack(
        [
            mo.hstack([visitors1, conversion1], justify="start"),
            mo.hstack([visitors2, conversion2], justify="start"),
            confidence,
            hypothesis,
        ],
    )
    return (
        confidence,
        conversion1,
        conversion2,
        hypothesis,
        visitors1,
        visitors2,
    )


@app.cell
def _(
    confidence,
    confint_proportions_2indep,
    conversion1,
    conversion2,
    hypothesis,
    power_proportions_2indep,
    test_proportions_2indep,
    visitors1,
    visitors2,
):
    count1 = conversion1.value
    count2 = conversion2.value
    nobs1 = visitors1.value
    nobs2 = visitors2.value
    p1 = count1 / nobs1
    p2 = count2 / nobs2
    alpha = 1 - confidence.value
    alternative = hypothesis.value

    tstats, pvalue = test_proportions_2indep(
        count1, nobs1, count2, nobs2, alternative=alternative
    )
    confint = confint_proportions_2indep(count1, nobs1, count2, nobs2, alpha=alpha)
    power = power_proportions_2indep(
        p1, p2, nobs1, nobs2, alpha=alpha, alternative=alternative
    )
    treatment_uplift = (p2 - p1) / p1
    return (
        alpha,
        alternative,
        confint,
        count1,
        count2,
        nobs1,
        nobs2,
        p1,
        p2,
        power,
        pvalue,
        treatment_uplift,
        tstats,
    )


@app.cell
def _(mo, pvalue):
    # Style.
    green = "#d4ffd4"
    red = "#ffd1d1"

    success = mo.md(
        f"""<span style='background-color: {green}'>The experiment is a success</span>"""
    )
    failure = mo.md(
        f"""<span style='background-color: {red}'>The experiment is not a success</span>"""
    )

    success if pvalue < 0.05 else failure
    return failure, green, red, success


@app.cell
def _(
    count1,
    count2,
    nobs1,
    nobs2,
    p1,
    p2,
    pl,
    power,
    pvalue,
    treatment_uplift,
    tstats,
):
    pl.DataFrame(
        {
            "variation": ["A", "B"],
            "users": [f"{count1:,}", f"{count2:,}"],
            "transactions": [f"{nobs1:,}", f"{nobs2:,}"],
            "conversion_rate": [f"{p1:.4f}", f"{p2:.4f}"],
            "z-value": [None, f"{-tstats:.4f}"],
            "p-value": [None, f"{pvalue:.4f}"],
            "uplift": [None, f"{treatment_uplift:.1%}"],
            "power": [None, f"{power:.1%}"],
        }
    )
    return


if __name__ == "__main__":
    app.run()
