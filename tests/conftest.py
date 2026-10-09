"""Shared test fixtures."""

import pytest

from data_prep.config import Settings

HOUSING_CSV = """\
sqft,bedrooms,price
1000,2,200000
1500,3,
2000,3,350000
1250,NA,240000
"""


@pytest.fixture
def housing_csv() -> str:
    """A small house-prices dataset, with a few missing cells."""
    return HOUSING_CSV


@pytest.fixture
def settings() -> Settings:
    """Test settings. The token is a placeholder, never a real credential."""
    return Settings(data_base_url="https://data.example.com", data_api_token="secret")
