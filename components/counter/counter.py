import pathlib
import anywidget
import traitlets

class CounterWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "index.js"
    _css = pathlib.Path(__file__).parent / "index.css"
    count = traitlets.Int(0).tag(sync=True)
