import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import anywidget
    import traitlets


    class ExampleWidget(anywidget.AnyWidget):
        # anywidget, required #
        _esm = """
        function render({ model, el }) {
            el.classList.add("custom-widget");
            function value_changed() {
                el.textContent = model.get("value");
            }
            value_changed();
            model.on("change:value", value_changed);
        }
        export default { render };
        """
        # anywidget, optional #
        _css = """
        .custom-widget {
            background-color: lightseagreen;
            padding: 0px 2px;
        }
        """
        # custom state for the widget #
        value = traitlets.Unicode("Hello World").tag(sync=True)


    widget = mo.ui.anywidget(ExampleWidget())
    widget
    return ExampleWidget, anywidget, mo, traitlets, widget


@app.cell
def _(widget):
    widget.value
    return


@app.cell
def _(widget):
    widget.value = "what"
    return


@app.cell
def _(mo):
    mo.md("""## Basic Image Viewer""")
    return


@app.cell
def _(anywidget, mo, traitlets):
    class ImageWidget(anywidget.AnyWidget):
        # anywidget, required #
        _esm = """
        function render({ model, el }) {
            const img = document.createElement('img')
            const div = document.createElement('div')
        
            img.src = model.get('value')
            img.onload = function() {
                div.innerHTML = img.width + " " + img.height
            }       
        
            el.appendChild(img)
            el.appendChild(div)

            model.on("change:value", () => {
                img.src = model.get('value')
            });
        }
        export default { render };
        """
        # anywidget, optional #
        _css = ""
        # custom state for the widget #
        value = traitlets.Unicode("").tag(sync=True)


    image = mo.ui.anywidget(ImageWidget())
    image
    return ImageWidget, image


@app.cell
def _(image):
    import base64
    from io import BytesIO
    from PIL import Image


    def load_base64_image(path: str) -> str:
        """utility to load and image and convert it to base64"""
        buffered = BytesIO()
        img = Image.open(path)
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return bytes("data:image/jpeg;base64,", encoding="utf-8") + img_str


    path = "public/images/orange.webp"
    image.value = load_base64_image(path)
    return BytesIO, Image, base64, load_base64_image, path


@app.cell
def _(ImageWidget, load_base64_image, mo):
    images = [
        "public/images/orange.webp",
        "public/images/apple.jpg",
        "public/images/banana.jpg",
    ]
    get_state, set_state = mo.state(0)

    slider = mo.ui.slider(
        0, len(images) - 1, value=get_state(), on_change=set_state
    )
    imager = mo.ui.anywidget(ImageWidget())
    imager.value = load_base64_image(images[get_state()])
    button = mo.ui.button(
        label="Next",
        on_click=lambda value: set_state(lambda n: (n + 1) % len(images)),
    )
    mo.vstack([slider, button, imager])
    return button, get_state, imager, images, set_state, slider


@app.cell
def _(get_state, imager, images, load_base64_image):
    imager.value = load_base64_image(images[get_state()])
    return


@app.cell
def _(mo):
    mo.md(r"""## Canvas Image Annotator""")
    return


@app.cell
def _(anywidget, traitlets):
    from traitlets import HasTraits, Int


    class ImageAnnotator(anywidget.AnyWidget):
        # anywidget, required #
        _esm = """
        class ImageAnnotation extends HTMLElement {
          constructor() {
            super();

            // Attach shadow DOM
            const shadow = this.attachShadow({ mode: 'open' });

            // Create container
            const container = document.createElement('div');
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.alignItems = 'center';

            // Create styles
            const style = document.createElement('style');
            style.textContent = `
              canvas {
                border: 1px solid #ccc;
                cursor: crosshair;
              }

              .controls {
                margin-bottom: 10px;
                display: flex;
                gap: 10px;
              }

              .controls button {
                padding: 5px 10px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 3px;
                cursor: pointer;
              }

              .controls button:hover {
                background-color: #0056b3;
              }
            `;

            // Create canvas
            const canvas = document.createElement('canvas');
            canvas.width = 400;
            canvas.height = 300;

            // Create controls
            const controls = document.createElement('div');
            controls.className = 'controls';

            const clearButton = document.createElement('button');
            clearButton.textContent = 'Clear Annotation';

            controls.appendChild(clearButton);

            // Append elements to container
            container.appendChild(controls);
            container.appendChild(canvas);

            // Append styles and container to shadow DOM
            shadow.appendChild(style);
            shadow.appendChild(container);

            // Canvas and context
            const ctx = canvas.getContext('2d');
            let isDrawing = false;
            let startX = 0;
            let startY = 0;
            let boundingBox = null; // Store a single bounding box
            let image = null;
            let label = '';

            // Start drawing bounding box
            canvas.addEventListener('mousedown', (event) => {
              const rect = canvas.getBoundingClientRect();
              startX = event.clientX - rect.left;
              startY = event.clientY - rect.top;
              isDrawing = true;
            });

            // Draw bounding box
            canvas.addEventListener('mousemove', (event) => {
              if (!image) return;

              const rect = canvas.getBoundingClientRect();
              const currentX = event.clientX - rect.left;
              const currentY = event.clientY - rect.top;

              // Clear the canvas and redraw the image
              ctx.clearRect(0, 0, canvas.width, canvas.height);
              ctx.drawImage(image, 0, 0);

              // Redraw the existing bounding box
              if (boundingBox) {
                ctx.strokeStyle = 'red';
                ctx.lineWidth = 2;
                ctx.strokeRect(boundingBox.x, boundingBox.y, boundingBox.width, boundingBox.height);
                
                ctx.fillStyle = 'red';
                ctx.font = '14px Arial';
                ctx.fillText(label, boundingBox.x + 5, boundingBox.y - 5);
              }

              if (isDrawing) {
                  // Draw the current bounding box
                  ctx.strokeStyle = 'blue';
                  ctx.lineWidth = 2;
                  ctx.strokeRect(startX, startY, currentX - startX, currentY - startY);
              
                  ctx.fillStyle = 'blue';
                  ctx.font = '14px Arial';
                  ctx.fillText(label, Math.min(startX, currentX) + 5, Math.min(startY, currentY) - 5);
              }

              // Draw guide lines
              ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
              ctx.lineWidth = 1;

              // Vertical line
              ctx.beginPath();
              ctx.moveTo(currentX, 0);
              ctx.lineTo(currentX, canvas.height);
              ctx.stroke();

              // Horizontal line
              ctx.beginPath();
              ctx.moveTo(0, currentY);
              ctx.lineTo(canvas.width, currentY);
              ctx.stroke();
            });

            // Finish drawing bounding box
            canvas.addEventListener('mouseup', (event) => {
              if (!isDrawing) return;

              const rect = canvas.getBoundingClientRect();
              const endX = event.clientX - rect.left;
              const endY = event.clientY - rect.top;

              const width = Math.abs(endX - startX);
              const height = Math.abs(endY - startY);

              // Store the single bounding box
              boundingBox = { x: Math.min(startX, endX), y: Math.min(startY, endY), width, height };

              isDrawing = false;

              // Redraw everything
              ctx.clearRect(0, 0, canvas.width, canvas.height);
              ctx.drawImage(image, 0, 0);
              ctx.strokeStyle = 'red';
              ctx.lineWidth = 2;
              ctx.strokeRect(boundingBox.x, boundingBox.y, boundingBox.width, boundingBox.height);
          
              ctx.fillStyle = 'red';
              ctx.font = '14px Arial';
              ctx.fillText(label, boundingBox.x + 5, boundingBox.y - 5);

              // Dispatch custom event
              this.dispatchEvent(new CustomEvent('boundingboxchange', {
                detail: boundingBox,
              }));
            });

            // Clear annotation
            clearButton.addEventListener('click', () => {
              boundingBox = null;
              if (image) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(image, 0, 0);
              }

              // Dispatch custom event for clearing
              this.dispatchEvent(new CustomEvent('boundingboxchange', {
                detail: null,
              }));
            });

            // Public method to set the image
            this.setImage = (imageSrc) => {
              const img = new Image();
              img.onload = () => {
                image = img;
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
              };
              img.src = imageSrc;
            };

            this.setLabel = (value) => {
                label = value
            }

            // Public method to get the bounding box data
            this.getBoundingBox = () => boundingBox;
          }
        }

        // Define the custom element
        if (!customElements.get('image-annotation')) customElements.define('image-annotation', ImageAnnotation);

        /*
        // Example usage
        const annotationTool = document.querySelector('image-annotation');
        annotationTool.setImage('public/images/apple.jpg'); // Replace with your image URL

        // Example: Get bounding box data
        setTimeout(() => {
          console.log(annotationTool.getBoundingBox());
        }, 10000); // Wait for user to draw a bounding box
        */

        function render({ model, el }) {
            const tool = document.createElement('image-annotation');
            tool.addEventListener('boundingboxchange', event => {
                model.set('boundingBox', event.detail);
                model.save_changes()
            })
            el.appendChild(tool)
            model.on("change:value", () => {
                tool.setImage(model.get('value'));
            });
            model.on("change:label", () => {
                tool.setLabel(model.get('label'));
            });
        }
        export default { render };
        """
        # anywidget, optional #
        _css = ""
        # custom state for the widget #
        value = traitlets.Unicode("").tag(sync=True)
        label = traitlets.Unicode("").tag(sync=True)
        boundingBox = traitlets.Dict(allow_none=True).tag(sync=True)
    return HasTraits, ImageAnnotator, Int


@app.cell
def _(ImageAnnotator, mo):
    import os
    import pathlib

    image_path = pathlib.Path("public/images")


    def handle_submit(value):
        if not marker.boundingBox:
            raise ValueError('bounding box is required')
        print(not marker.boundingBox)
        print(radio.value)
        print(marker.boundingBox)


    def set_label(value):
        marker.label = value


    marker = mo.ui.anywidget(ImageAnnotator())
    radio = mo.ui.radio(options=os.listdir(str(image_path)), label="Select Image")
    marker = mo.ui.anywidget(ImageAnnotator())
    label = mo.ui.text(label="Enter label", on_change=set_label)
    submit = mo.ui.button(label="Submit", on_click=handle_submit)

    mo.vstack([radio, label, submit, marker])
    return (
        handle_submit,
        image_path,
        label,
        marker,
        os,
        pathlib,
        radio,
        set_label,
        submit,
    )


@app.cell
def _(image_path, load_base64_image, marker, radio):
    marker.value = load_base64_image(str(image_path / radio.value))
    return


@app.cell
def _(marker):
    marker.boundingBox
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
