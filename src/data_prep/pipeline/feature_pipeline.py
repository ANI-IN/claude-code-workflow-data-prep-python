"""Column processing. Today it reads a numeric column and returns the
values unchanged.

FEATURE TASK (for the Explore -> Plan -> Code -> Commit exercise):
Add min-max scaling here. Before training, numeric features should be
scaled into the range [0, 1], so a feature with a large range (square
footage) does not drown out one with a small range (bedrooms).

Success criteria:
  - prepare_column() can return min-max scaled values in [0, 1].
  - The original values are still available.
  - pytest passes (tests/ is the source of truth).
"""

import csv
import io
import math
from typing import Literal, get_args

Scaling = Literal["none", "minmax"]  # minmax not implemented yet

SUPPORTED_SCALINGS: tuple[str, ...] = get_args(Scaling)

MISSING_MARKERS = frozenset({"", "na", "n/a", "nan", "null"})

Column = list[float | None]


def read_column(csv_text: str, column: str) -> list[str]:
    """Return the raw cell values of ``column`` from ``csv_text``."""
    reader = csv.DictReader(io.StringIO(csv_text))
    if reader.fieldnames is None or column not in reader.fieldnames:
        raise ValueError(f"Unknown column: {column!r}")
    return [row[column] or "" for row in reader]


def parse_numeric(cells: list[str]) -> Column:
    """Convert raw cells to floats. Missing cells become ``None``."""
    values: Column = []
    for cell in cells:
        text = cell.strip()
        if text.lower() in MISSING_MARKERS:
            values.append(None)
            continue
        try:
            value = float(text)
        except ValueError:
            raise ValueError(f"Not a number: {cell!r}") from None
        if not math.isfinite(value):
            raise ValueError(f"Not a finite number: {cell!r}")
        values.append(value)
    return values


def prepare_column(values: Column, *, scaling: Scaling = "none") -> Column:
    """Return ``values`` scaled with ``scaling``. Missing values stay ``None``."""
    if scaling not in SUPPORTED_SCALINGS:
        raise ValueError(f"Unsupported scaling: {scaling!r}")
    if scaling == "minmax":
        raise NotImplementedError("Min-max scaling not implemented yet")
    # no scaling today
    return list(values)
