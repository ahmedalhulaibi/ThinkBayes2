#!/usr/bin/env python3
"""Convert the chapter Jupyter notebooks to marimo Python notebooks."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    sources = sorted((ROOT / "notebooks").glob("chap*.ipynb"))
    if not sources:
        raise SystemExit("No chapter notebooks found in notebooks/.")

    for source in sources:
        output = source.with_suffix(".py")
        subprocess.run(
            ["uvx", "marimo", "convert", str(source), "-o", str(output)],
            check=True,
        )
        print(f"{source.relative_to(ROOT)} -> {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
