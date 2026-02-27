"""Path helpers for consistent local and container execution."""

from pathlib import Path


def project_root() -> Path:
    """Return the repository root from package location."""
    return Path(__file__).resolve().parents[2]


def data_csv_path() -> Path:
    """Return preferred dataset path with legacy fallback."""
    root = project_root()
    candidates = [
        root / "data" / "raw" / "gallstone.csv",
        root / "gallstone.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def notebook_path() -> Path:
    """Return canonical notebook path."""
    return project_root() / "notebooks" / "gallstone_final_project.ipynb"
