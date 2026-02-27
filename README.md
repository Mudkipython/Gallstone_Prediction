# Gallstone Risk Prediction Showcase

Notebook-first clinical ML showcase for **non-imaging gallstone risk prediction** using routine checkup variables.

## What This Project Includes
- A reproducible notebook pipeline for analysis and model comparison.
- An English Streamlit Web App for interactive risk estimation.
- Dockerized runtime for portable execution.
- Basic engineering quality gates (`ruff`, `mypy`, `pytest`).
- Notebook-aligned private-clinic feature policy with engineered lipid ratios.

## Learning Outcomes
- Build a reproducible ML workflow with modern Python tooling (`uv`, `ruff`, `mypy`, `pytest`).
- Train and evaluate binary classifiers for clinical risk stratification.
- Preserve interpretable outputs (calibration, SHAP, subgroup diagnostics).

## Prerequisites
- Python 3.12
- `uv` 0.10+
- Optional: Docker 29+

## Project Layout
- `notebooks/gallstone_final_project.ipynb`: primary analysis notebook.
- `data/raw/gallstone.csv`: source dataset.
- `src/gallstone_showcase/model.py`: training/inference helpers used by the Web App.
- `src/gallstone_showcase/webapp.py`: Streamlit app (English UI).
- `scripts/run_notebook.py`: headless notebook execution entrypoint.
- `scripts/smoke_check.py`: quick dependency/data validation.
- `artifacts/`: generated outputs (executed notebook and future artifacts).
- `docs/presentation.pdf`: project presentation deck.

## Quickstart
```bash
make sync
make smoke
make run
```

`make run` generates:
- `artifacts/notebooks/gallstone_final_project.executed.ipynb`

## Launch Interfaces

### 1) Notebook (Jupyter Lab)
```bash
make notebook
```
Open: `http://localhost:8888`

### 2) Web App (Streamlit, English)
```bash
make webapp
```
Open: `http://localhost:8501`

The app follows the updated notebook policy:
- engineered features: `LDL_to_HDL`, `TC_to_HDL`, `TG_to_HDL`, `Age_x_BMI`
- excluded leakage features: `AST`, `ALT`, `ALP`, `CRP`, `AST_to_ALT`

## Script Entry Point (Explicit Timeout)
```bash
uv run python scripts/run_notebook.py \
  --notebook notebooks/gallstone_final_project.ipynb \
  --output artifacts/notebooks/gallstone_final_project.executed.ipynb \
  --timeout 600
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

Open: `http://localhost:8888`

## Deployment Note
Because this project has a Docker image, it can be deployed to container platforms (e.g., Azure Container Apps / AKS / ACI). For production, consider replacing Jupyter entrypoint with a FastAPI service.

## Common Issues
- Missing dependencies: run `make sync`.
- Missing dataset: verify `data/raw/gallstone.csv` exists.
- Notebook currently uses `DATA_PATH='gallstone.csv'`:
  - `make notebook` auto-creates a compatibility symlink at repo root.
  - `make run` handles compatibility automatically in `scripts/run_notebook.py`.
- Notebook timeout on slower hardware:
  - default is `NOTEBOOK_TIMEOUT=1800`
  - override with `make run NOTEBOOK_TIMEOUT=2400`
- macOS LightGBM error (`libomp.dylib` not found):
  - run `brew install libomp`

## Important Disclaimer
This project is for research/education and demonstration only. It is **not** a medical diagnosis tool.
