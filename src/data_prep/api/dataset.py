"""Public route: validates the request, downloads the dataset, prepares a column."""

import re

from data_prep.config import Settings
from data_prep.integrations.dataset_source import fetch_csv
from data_prep.pipeline.feature_pipeline import (
    Column,
    Scaling,
    parse_numeric,
    prepare_column,
    read_column,
)

DATASET_NAME_PATTERN = re.compile(r"[a-zA-Z0-9_-]{1,64}")


def handle_prepare(
    dataset: str, column: str, settings: Settings, *, scaling: Scaling = "none"
) -> Column:
    """Return the values of ``column`` from ``dataset``, scaled with ``scaling``."""
    if not DATASET_NAME_PATTERN.fullmatch(dataset):
        raise ValueError("Invalid dataset name")
    csv_text = fetch_csv(
        dataset, base_url=settings.data_base_url, token=settings.data_api_token
    )
    values = parse_numeric(read_column(csv_text, column))
    return prepare_column(values, scaling=scaling)
