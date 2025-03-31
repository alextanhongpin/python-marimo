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
        sample_size_for_proportions,
        test_proportions_2indep,
    )

    return (
        confint_proportions_2indep,
        math,
        mo,
        pl,
        power_proportions_2indep,
        sample_size_for_proportions,
        test_proportions_2indep,
    )


@app.cell
def _(mo):
    mo.md("""# Sample size calculator""")
    return


@app.cell
def _(mo):
    conversion_control = mo.ui.number(value=0.02, label="Conversion rate Control")
    uplift = mo.ui.number(value=15, label="Expected uplift (in %)")

    mo.vstack([conversion_control, uplift])
    return conversion_control, uplift


@app.cell
def _(conversion_control, mo, sample_size_for_proportions, uplift):
    conversion_treatment = float(
        (uplift.value + 100) / 100.0 * conversion_control.value
    )

    sample_size = sample_size_for_proportions(
        conversion_control.value, conversion_treatment
    )
    mo.md(f"## Sample size of **{sample_size:,}** is required")
    return conversion_treatment, sample_size


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

    mo.vstack(
        [
            mo.hstack([visitors1, conversion1], justify="start"),
            mo.hstack([visitors2, conversion2], justify="start"),
        ]
    )
    return conversion1, conversion2, visitors1, visitors2


@app.cell
def _(
    confint_proportions_2indep,
    conversion1,
    conversion2,
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

    tstats, pvalue = test_proportions_2indep(count1, nobs1, count2, nobs2)
    confint = confint_proportions_2indep(count1, nobs1, count2, nobs2)
    power = power_proportions_2indep(p1, p2, nobs1, nobs2)
    treatment_uplift = (p2 - p1) / p1
    return (
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
