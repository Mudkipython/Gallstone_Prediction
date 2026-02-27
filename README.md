# Gallstone Risk Prediction Showcase

Notebook-first clinical ML showcase for non-imaging gallstone risk prediction using routine checkup variables.

## Learning Outcomes
- Build a reproducible notebook workflow with modern Python project tooling (`uv`, `ruff`, `mypy`, `pytest`).
- Train and compare multiple binary classifiers for gallstone risk stratification.
- Preserve interpretable analysis outputs (calibration, SHAP, subgroup diagnostics) in a reproducible structure.

## Prerequisites
- Python 3.12
- `uv` 0.10+
- Optional: Docker 29+

## Project Structure
- `notebooks/gallstone_final_project.ipynb`: primary analysis notebook.
- `data/raw/gallstone.csv`: source dataset.
- `scripts/run_notebook.py`: headless notebook execution entrypoint.
- `scripts/smoke_check.py`: quick dependency/data validation.
- `src/gallstone_showcase/`: lightweight path utilities for stable execution contexts.
- `artifacts/`: generated outputs (executed notebooks and derived files).
- `docs/presentation.pdf`: project presentation deck.

## Quickstart
```bash
make sync
make smoke
make run
```

To launch Jupyter Lab:
```bash
make notebook
```

Script entrypoint (explicit timeout):
```bash
uv run python scripts/run_notebook.py --notebook notebooks/gallstone_final_project.ipynb --output artifacts/notebooks/gallstone_final_project.executed.ipynb --timeout 600
```

## Quality Gates
```bash
make ruff
make ty
make test
make check
```

## Docker Runtime
Build image:
```bash
make docker-build
```

Run Jupyter in container:
```bash
make docker-run
```

Then open `http://localhost:8888`.

## Key Artifacts
- `artifacts/notebooks/gallstone_final_project.executed.ipynb`: executed notebook output from `make run`.

## Common Failure Modes
- Missing dependencies: run `make sync` again.
- Missing dataset: confirm `data/raw/gallstone.csv` exists.
- Notebook timeout on slower hardware: increase `--timeout` in `scripts/run_notebook.py` invocation.
- `make run` uses `NOTEBOOK_TIMEOUT` (default `1800`); override with `make run NOTEBOOK_TIMEOUT=600` if needed.

## Suggested Next Steps
- Extract reusable preprocessing/model-evaluation logic from notebook into `src/gallstone_showcase/`.
- Add explicit artifact verification script and manifest for stricter contract checks.
