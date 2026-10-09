"""The source of truth for "correct" in the feature pipeline."""

import pytest

from data_prep.pipeline.feature_pipeline import (
    parse_numeric,
    prepare_column,
    prepare_column_keeping_original,
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


def test_minmax_scales_values_into_the_unit_range() -> None:
    assert prepare_column([1000.0, 1500.0, 2000.0], scaling="minmax") == [
        0.0,
        0.5,
        1.0,
    ]


def test_minmax_keeps_missing_values_in_place() -> None:
    assert prepare_column([10.0, None, 20.0], scaling="minmax") == [0.0, None, 1.0]


def test_minmax_handles_negative_values() -> None:
    assert prepare_column([-5.0, 0.0, 5.0], scaling="minmax") == [0.0, 0.5, 1.0]


def test_minmax_output_stays_in_the_unit_range(housing_csv: str) -> None:
    prices = parse_numeric(read_column(housing_csv, "price"))
    scaled = prepare_column(prices, scaling="minmax")
    present = [value for value in scaled if value is not None]
    assert min(present) == 0.0
    assert max(present) == 1.0
    assert all(0.0 <= value <= 1.0 for value in present)


def test_minmax_on_a_constant_column_returns_zeros() -> None:
    assert prepare_column([3.0, 3.0, None, 3.0], scaling="minmax") == [
        0.0,
        0.0,
        None,
        0.0,
    ]


@pytest.mark.parametrize("values", [[], [None, None]])
def test_minmax_on_a_column_with_no_values_is_unchanged(
    values: list[float | None],
) -> None:
    assert prepare_column(values, scaling="minmax") == values


def test_minmax_does_not_modify_the_input() -> None:
    values: list[float | None] = [1000.0, 1500.0, 2000.0]
    prepare_column(values, scaling="minmax")
    assert values == [1000.0, 1500.0, 2000.0]


def test_minmax_scaling_keeps_the_original_values() -> None:
    result = prepare_column_keeping_original([1000.0, None, 2000.0], scaling="minmax")
    assert result.original == (1000.0, None, 2000.0)
    assert result.output == (0.0, None, 1.0)
    assert result.scaling == "minmax"


def test_keeping_original_without_scaling_returns_the_same_values() -> None:
    result = prepare_column_keeping_original([1.0, None])
    assert result.original == result.output == (1.0, None)
