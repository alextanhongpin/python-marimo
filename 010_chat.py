import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    def chat(messages, config):
        last_message = messages[-1]
        return "Echo: " + last_message.content


    mo.ui.chat(chat)
    return (chat,)


@app.cell
def _(mo):
    chatbot = mo.ui.chat(
        mo.ai.llm.openai(
            model="llama3.2",
            api_key="ollama",  # insert your key here
            base_url="http://localhost:11434/v1",
        ),
    )
    chatbot
    return (chatbot,)


if __name__ == "__main__":
    app.run()
