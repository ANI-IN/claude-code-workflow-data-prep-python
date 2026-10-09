"""Column processing. Reads a numeric column and can min-max scale it into
the range [0, 1] while keeping the original values available.

This is the completed result of the Explore -> Plan -> Code -> Commit
exercise. The feature added here is min-max scaling, so a feature with a
large range (square footage) does not drown out one with a small range
(bedrooms).

Success criteria (all met):
  - prepare_column() can return min-max scaled values in [0, 1].
  - The original values are still available.
  - pytest passes (tests/ is the source of truth).
"""

import csv
import io
import math
from dataclasses import dataclass
from typing import Literal, get_args

Scaling = Literal["none", "minmax"]

SUPPORTED_SCALINGS: tuple[str, ...] = get_args(Scaling)

MISSING_MARKERS = frozenset({"", "na", "n/a", "nan", "null"})

Column = list[float | None]


@dataclass(frozen=True)
class PreparedColumn:
    """The original column values alongside their prepared copy."""

    original: tuple[float | None, ...]
    output: tuple[float | None, ...]
    scaling: Scaling


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


def minmax_scale(values: Column) -> Column:
    """Scale ``values`` into [0, 1]: the minimum maps to 0 and the maximum to 1.

    Missing values stay ``None`` in the same positions and are ignored when
    finding the minimum and maximum. A constant column has no range to scale
    by, so every present value maps to 0.0 instead of dividing by zero.
    """
    present = [value for value in values if value is not None]
    if not present:
        return list(values)
    low, high = min(present), max(present)
    span = high - low
    if span == 0:
        return [None if value is None else 0.0 for value in values]
    return [None if value is None else (value - low) / span for value in values]


def prepare_column(values: Column, *, scaling: Scaling = "none") -> Column:
    """Return a new list of ``values`` scaled with ``scaling``.

    Missing values stay ``None``, and ``values`` itself is never modified.
    """
    if scaling not in SUPPORTED_SCALINGS:
        raise ValueError(f"Unsupported scaling: {scaling!r}")
    if scaling == "minmax":
        return minmax_scale(values)
    # no scaling
    return list(values)


def prepare_column_keeping_original(
    values: Column, *, scaling: Scaling = "none"
) -> PreparedColumn:
    """Prepare ``values`` and return them together with the untouched original."""
    output = prepare_column(values, scaling=scaling)
    return PreparedColumn(original=tuple(values), output=tuple(output), scaling=scaling)
