#!/usr/bin/env python
"""Execute a notebook and persist the executed output."""

from __future__ import annotations

import argparse
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

    with notebook.open("r", encoding="utf-8") as handle:
        nb = nbformat.read(handle, as_version=4)

    client = NotebookClient(nb, timeout=args.timeout, kernel_name="python3")
    client.execute(cwd=str(root))

    with output.open("w", encoding="utf-8") as handle:
        nbformat.write(nb, handle)


if __name__ == "__main__":
    main()
