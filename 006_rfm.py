import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import random
    import datetime
    import polars as pl
    import plotly.express as px

    random.seed(0)
    return datetime, mo, np, pl, px, random


@app.cell
def _(datetime, pl, random):
    # Algorithm for RFM
    def random_date(
        start: datetime.datetime, delta: datetime.timedelta
    ) -> datetime.datetime:
        return start + datetime.timedelta(
            seconds=random.randint(0, int(delta.total_seconds()))
        )


    n = 100
    start = datetime.datetime(2025, 1, 1, 0, 0)
    delta = datetime.timedelta(days=30)


    df = pl.DataFrame(
        {
            "invoice_date": sorted([random_date(start, delta) for _ in range(n)]),
            "customer_id": sorted([random.randint(1, 50) for _ in range(n)]),
            "invoice_no": sorted([i + 1 for i in range(n)]),
            "quantity": [random.randint(1, 3) for _ in range(n)],
            "unit_price": [random.choice([5, 10, 15]) for _ in range(n)],
        }
    )
    df
    return delta, df, n, random_date, start


@app.cell
def _(pl):
    def rfm(data):
        # Recency
        data = data.with_columns(
            recency=data["invoice_date"].max().day - data["invoice_date"].dt.day()
        )

        # Frequency
        frequency = data.group_by("customer_id").agg(
            pl.col("invoice_no").count().alias("frequency")
        )
        data = data.join(frequency, on="customer_id", how="left")

        # Monetary
        data = data.with_columns(monetary=data["quantity"] * data["unit_price"])
        monetary = data.group_by("customer_id").agg(pl.col("monetary").sum())
        data = data.join(monetary, on="customer_id", how="left")
        return data.select(
            pl.col("customer_id", "recency", "frequency", "monetary")
        )
    return (rfm,)


@app.cell
def _(df, rfm):
    out_df = rfm(df)
    out_df
    return (out_df,)


@app.cell
def _(out_df, pl):
    bin_df = pl.DataFrame().with_columns(
        customer_id=out_df["customer_id"],
        recency_bin=out_df["recency"].qcut(3, labels=["high", "medium", "low"]),
        frequency_bin=out_df["frequency"].qcut(
            3, labels=["low", "medium", "high"]
        ),
        monetary_bin=out_df["monetary"].qcut(3, labels=["low", "medium", "high"]),
    )
    bin_df
    return (bin_df,)


@app.cell
def _(bin_df, pl):
    bin_df.filter(
        (pl.col("recency_bin") == "low")
        & (pl.col("frequency_bin") == "low")
        & (pl.col("monetary_bin") == "high")
    )
    return


@app.cell
def _(out_df, px):
    px.scatter_3d(
        out_df, x="recency", y="frequency", z="monetary", color="customer_id"
    )
    return


if __name__ == "__main__":
    app.run()
