#!/usr/bin/env python
"""Run lightweight checks for local reproducibility."""

from __future__ import annotations

import importlib
from pathlib import Path

import pandas as pd

from gallstone_showcase.paths import data_csv_path


def ensure_imports() -> None:
    modules = [
        "numpy",
        "pandas",
        "scipy",
        "matplotlib",
        "seaborn",
        "sklearn",
        "lightgbm",
        "xgboost",
        "statsmodels",
        "shap",
    ]
    for module in modules:
        importlib.import_module(module)


def ensure_dataset(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    frame = pd.read_csv(path)
    if frame.empty:
        raise ValueError("Dataset is empty")
    if frame.shape[1] == 0:
        raise ValueError("Dataset has no columns")


def main() -> None:
    ensure_imports()
    ensure_dataset(data_csv_path())
    print("Smoke check passed")


if __name__ == "__main__":
    main()
