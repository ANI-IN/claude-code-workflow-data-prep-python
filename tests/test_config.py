"""Tests for settings loading."""

import pytest

from data_prep.config import load_settings


def test_settings_are_read_from_the_environment() -> None:
    settings = load_settings(
        {"DATA_BASE_URL": "https://data.example.com", "DATA_API_TOKEN": "t"}
    )
    assert settings.data_base_url == "https://data.example.com"
    assert settings.data_api_token == "t"


def test_missing_token_is_an_error() -> None:
    with pytest.raises(RuntimeError, match="DATA_API_TOKEN"):
        load_settings({"DATA_BASE_URL": "https://data.example.com"})
