import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from lib.ab import sample_size_for_proportions, test_proportions_2indep
    return sample_size_for_proportions, test_proportions_2indep


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
    mo.md(
        f"## Sample size of **{sample_size}** is required to achieve conversion of {conversion_treatment}"
    )
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
    conversion1,
    conversion2,
    mo,
    test_proportions_2indep,
    visitors1,
    visitors2,
):
    tstats, pvalue = test_proportions_2indep(
        conversion1.value, conversion2.value, visitors1.value, visitors2.value
    )

    result = "The result is not significant"
    if pvalue < 0.05:
        result = "The result is statistically significant"


    mo.md(f"""
    t-stats: **{tstats}**

    p-value: **{pvalue}**

    {result}
    """)
    return pvalue, result, tstats


if __name__ == "__main__":
    app.run()
