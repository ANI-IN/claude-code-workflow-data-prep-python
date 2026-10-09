"""The source of truth for "correct". The min-max test is written to fail
until the feature is implemented during the Code step."""

import pytest

from data_prep.pipeline.feature_pipeline import (
    parse_numeric,
    prepare_column,
    read_column,
)


def test_read_column_returns_raw_cells(housing_csv: str) -> None:
    assert read_column(housing_csv, "sqft") == ["1000", "1500", "2000", "1250"]


def test_unknown_column_is_rejected(housing_csv: str) -> None:
    with pytest.raises(ValueError, match="Unknown column"):
        read_column(housing_csv, "garage")


def test_parse_numeric_turns_missing_cells_into_none() -> None:
    cells = ["3", " 2.5 ", "", "NA", "n/a"]
    assert parse_numeric(cells) == [3.0, 2.5, None, None, None]


@pytest.mark.parametrize("cell", ["three", "1,000", "inf", "nan1"])
def test_parse_numeric_rejects_bad_cells(cell: str) -> None:
    with pytest.raises(ValueError, match="number"):
        parse_numeric([cell])


def test_no_scaling_returns_the_values() -> None:
    values = [1000.0, None, 2000.0]
    assert prepare_column(values, scaling="none") == values


def test_no_scaling_is_the_default() -> None:
    assert prepare_column([1.0, 2.0]) == [1.0, 2.0]


def test_unsupported_scaling_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported scaling"):
        prepare_column([1.0], scaling="zscore")  # type: ignore[arg-type]


# This should pass once min-max scaling is implemented.
def test_minmax_scales_values_into_the_unit_range() -> None:
    assert prepare_column([1000.0, 1500.0, 2000.0], scaling="minmax") == [
        0.0,
        0.5,
        1.0,
    ]
