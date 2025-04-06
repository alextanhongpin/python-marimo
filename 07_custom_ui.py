import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import anywidget
    import traitlets
    import marimo as mo


    class CounterWidget(anywidget.AnyWidget):
        # Widget front-end JavaScript code
        _esm = """
        function render({ model, el }) {
          let getCount = () => model.get("count");
          let button = document.createElement("button");
          button.innerHTML = `count is ${getCount()}`;
          button.addEventListener("click", () => {
            model.set("count", getCount() + 1);
            model.save_changes();
          });
          model.on("change:count", () => {
            button.innerHTML = `count is ${getCount()}`;
          });
          el.appendChild(button);
        }
        export default { render };
      """
        _css = """
        button {
          padding: 5px !important;
          border-radius: 5px !important;
          background-color: #f0f0f0 !important;

          &:hover {
            background-color: lightblue !important;
            color: white !important;
          }
        }
      """

        # Stateful property that can be accessed by JavaScript & Python
        count = traitlets.Int(0).tag(sync=True)


    widget = mo.ui.anywidget(CounterWidget())
    widget
    return CounterWidget, anywidget, mo, traitlets, widget


@app.cell
def _(widget):
    # In another cell, you can access the widget's value
    widget.value

    # You can also access the widget's specific properties
    widget.count
    return


@app.cell
def _():
    from components.counter.counter import CounterWidget as CounterWidget2
    return (CounterWidget2,)


@app.cell
def _(CounterWidget2, mo):
    counter = mo.ui.anywidget(CounterWidget2())
    counter
    return (counter,)


@app.cell
def _(counter):
    counter.value
    return


@app.cell
def _(counter):
    counter.count
    return


if __name__ == "__main__":
    app.run()
