"""Tests for the dataset source. No real network calls are made."""

import io
from typing import Any
from urllib.request import Request

import pytest

from data_prep.integrations import dataset_source


def test_fetch_csv_uses_tls_and_bearer_token(
    housing_csv: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, Any] = {}

    def fake_urlopen(request: Request, timeout: float) -> io.BytesIO:
        captured["request"] = request
        captured["timeout"] = timeout
        return io.BytesIO(housing_csv.encode("utf-8"))

    monkeypatch.setattr(dataset_source, "urlopen", fake_urlopen)
    text = dataset_source.fetch_csv(
        "housing", base_url="https://data.example.com/", token="secret"
    )

    request: Request = captured["request"]
    assert text == housing_csv
    assert request.full_url == "https://data.example.com/datasets/housing.csv"
    assert request.unredirected_hdrs["Authorization"] == "Bearer secret"
    # Redirected requests copy only request.headers, so the token must not be there.
    assert "Authorization" not in request.headers
    assert captured["timeout"] == dataset_source.REQUEST_TIMEOUT_SECONDS


def test_plain_http_store_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_if_called(request: Request, timeout: float) -> io.BytesIO:
        raise AssertionError("an insecure store must not be contacted")

    monkeypatch.setattr(dataset_source, "urlopen", fail_if_called)
    with pytest.raises(ValueError, match="HTTPS"):
        dataset_source.fetch_csv(
            "housing", base_url="http://data.example.com", token="secret"
        )
