SHELL := /bin/bash
.DEFAULT_GOAL := help

NOTEBOOK := notebooks/gallstone_final_project.ipynb
EXEC_NOTEBOOK := artifacts/notebooks/gallstone_final_project.executed.ipynb
NOTEBOOK_TIMEOUT ?= 1800

.PHONY: help sync run notebook smoke ruff test ty check docker-build docker-run

help:
	@echo "Gallstone Showcase"
	@echo "  make sync         Install dependencies with uv"
	@echo "  make run          Execute notebook headlessly"
	@echo "  make notebook     Launch Jupyter Lab"
	@echo "  make smoke        Run lightweight data/import checks"
	@echo "  make ruff         Run Ruff lint checks"
	@echo "  make test         Run pytest"
	@echo "  make ty           Run mypy"
	@echo "  make check        Run ruff + mypy + pytest"
	@echo "  make docker-build Build notebook runtime image"
	@echo "  make docker-run   Run notebook runtime container"

sync:
	uv sync --extra dev

run:
	uv run python scripts/run_notebook.py --notebook $(NOTEBOOK) --output $(EXEC_NOTEBOOK) --timeout $(NOTEBOOK_TIMEOUT)

notebook:
	uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --ServerApp.token='' --ServerApp.password=''

smoke:
	uv run python scripts/smoke_check.py

ruff:
	uv run ruff check .

test:
	uv run pytest

ty:
	uv run mypy

check: ruff ty test

docker-build:
	docker build -t gallstone-showcase .

docker-run:
	docker run --rm -p 8888:8888 -v "$(PWD)":/workspace gallstone-showcase
