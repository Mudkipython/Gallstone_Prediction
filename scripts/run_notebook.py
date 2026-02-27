#!/usr/bin/env python
"""Execute a notebook and persist the executed output."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import nbformat
from nbclient import NotebookClient

from gallstone_showcase.paths import project_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute a notebook headlessly.")
    parser.add_argument("--notebook", required=True, help="Input notebook path")
    parser.add_argument("--output", required=True, help="Output notebook path")
    parser.add_argument("--timeout", type=int, default=600, help="Execution timeout per cell")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = project_root()
    notebook = Path(args.notebook)
    output = Path(args.output)

    if not notebook.is_absolute():
        notebook = root / notebook
    if not output.is_absolute():
        output = root / output

    output.parent.mkdir(parents=True, exist_ok=True)
    legacy_data = root / "gallstone.csv"
    canonical_data = root / "data" / "raw" / "gallstone.csv"
    created_legacy = False

    if not legacy_data.exists() and canonical_data.exists():
        try:
            legacy_data.symlink_to(canonical_data.relative_to(root))
        except OSError:
            shutil.copy2(canonical_data, legacy_data)
        created_legacy = True

    try:
        with notebook.open("r", encoding="utf-8") as handle:
            nb = nbformat.read(handle, as_version=4)

        client = NotebookClient(nb, timeout=args.timeout, kernel_name="python3")
        client.execute(cwd=str(root))

        with output.open("w", encoding="utf-8") as handle:
            nbformat.write(nb, handle)
    finally:
        if created_legacy and legacy_data.exists():
            legacy_data.unlink()


if __name__ == "__main__":
    main()
