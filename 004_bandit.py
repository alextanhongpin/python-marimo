import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from lib.bandit import Bandit
    return Bandit, mo


@app.cell
def _():
    fruits = {
        "apple": "public/images/apple.jpg",
        "banana": "public/images/banana.jpg",
        "orange": "public/images/orange.webp",
    }

    fruit_items = list(fruits.items())
    return fruit_items, fruits


@app.cell
def _(Bandit, fruit_items, mo):
    bandit = Bandit(len(fruit_items))

    get_arm, set_arm = mo.state(bandit.pull())
    return bandit, get_arm, set_arm


@app.cell
def _(fruit_items, fruits, get_arm, mo):
    fruit, image = fruit_items[get_arm()]
    get_state, set_state = mo.state(0)
    ok = mo.ui.button(value=1, on_change=set_state, kind="success", label="OK")
    cancel = mo.ui.button(
        value=-1, on_change=set_state, kind="neutral", label="Cancel"
    )

    mo.vstack(
        [
            mo.image(
                fruits[fruit], alt=fruit, width=320, rounded=True, caption=fruit
            ),
            mo.hstack([ok, cancel], justify="start"),
        ]
    )
    return cancel, fruit, get_state, image, ok, set_state


@app.cell
def _(bandit, fruit_items, get_arm, get_state, mo, set_arm, set_state):
    if get_state() != 0:
        bandit.update(get_arm(), get_state() == 1)
        set_state(0)
        set_arm(bandit.pull())


    texts = []
    for i in range(len(fruit_items)):
        name = fruit_items[i][0]
        impressions = bandit.impressions[i]
        success, failure = bandit.engagements[i]
        texts.append(
            f"{name} shown {impressions} times (clicked={success}, not clicked={failure})"
        )

    mo.vstack([mo.md(text) for text in texts])
    return failure, i, impressions, name, success, texts


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
