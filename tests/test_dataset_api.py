"""Tests for the public dataset route."""

import pytest

from data_prep.api import dataset
from data_prep.config import Settings


@pytest.mark.parametrize(
    "name",
    ["", "../secrets", "housing.csv", "house prices", "x" * 65],
)
def test_invalid_dataset_name_is_rejected(
    name: str, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_if_called(name: str, *, base_url: str, token: str) -> str:
        raise AssertionError("the store must not be contacted for an invalid name")

    monkeypatch.setattr(dataset, "fetch_csv", fail_if_called)
    with pytest.raises(ValueError, match="Invalid dataset name"):
        dataset.handle_prepare(name, "sqft", settings)


def test_valid_request_fetches_and_prepares_the_column(
    housing_csv: str, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[str, str, str]] = []

    def fake_fetch(name: str, *, base_url: str, token: str) -> str:
        calls.append((name, base_url, token))
        return housing_csv

    monkeypatch.setattr(dataset, "fetch_csv", fake_fetch)
    assert dataset.handle_prepare("housing", "price", settings) == [
        200000.0,
        None,
        350000.0,
        240000.0,
    ]
    assert calls == [("housing", "https://data.example.com", "secret")]
