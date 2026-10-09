"""Runtime settings, read from environment variables."""

import os
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Where the dataset store lives and how to authenticate to it."""

    data_base_url: str
    data_api_token: str


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    """Build ``Settings`` from ``env`` (defaults to ``os.environ``).

    The token is never hardcoded; it must come from the environment.
    """
    source = os.environ if env is None else env
    try:
        return Settings(
            data_base_url=source["DATA_BASE_URL"],
            data_api_token=source["DATA_API_TOKEN"],
        )
    except KeyError as exc:
        raise RuntimeError(f"Missing required setting: {exc.args[0]}") from exc
