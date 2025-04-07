import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import sqlmodel

    DATABASE_URL = "sqlite:///test.dbv"
    engine = sqlmodel.create_engine(DATABASE_URL)
    return DATABASE_URL, engine, sqlmodel


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        drop table users;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        create table users (
            id integer primary key autoincrement,
            name text,
            unique (name)
        );
        """,
        engine=engine
    )
    return


@app.cell
def _():
    jane = "jane"
    return (jane,)


@app.cell
def _(engine, jane, mo, users):
    _df = mo.sql(
        f"""
        insert into users(name) values ('john'), ('{jane}');
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, users):
    user_rows = mo.sql(
        f"""
        SELECT * FROM users
        """,
        engine=engine
    )
    return (user_rows,)


@app.cell
def _(user_rows):
    user_rows.to_dicts()
    return


@app.cell
def _(mo):
    form = (
        mo.md("""
    ## Create User

    Name: {name}
    """)
        .batch(name=mo.ui.text())
        .form(clear_on_submit=True)
    )
    form
    return (form,)


@app.cell
def _(engine, form, mo, users):
    _df = mo.sql(
        f"""
        insert into users(name) values ('{form.value["name"]}') returning id
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, users):
    _df = mo.sql(
        f"""
        select * from users;
        """,
        engine=engine
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
