PYTHON ?= python

.PHONY: run test

run:
	uv run $(PYTHON) -m llm_cursor.cli

test:
	uv run pytest

