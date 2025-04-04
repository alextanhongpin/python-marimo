-include .env
export

marimo: 
	@uv run marimo edit


run:
	@uv run marimo run $(name)


install:
	curl -LsSf https://astral.sh/uv/install.sh | sh

lint:
	#uv run mypy --install-types
	@uvx ruff format
	@uvx ruff check --fix --select I
	@uv run mypy . # uvx runs in separate virtual environment.


build:
	./build.sh

run:
	open http://localhost:8000
	uv run python -m http.server 8000
