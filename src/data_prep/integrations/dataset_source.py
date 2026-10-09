"""Downloads a CSV dataset from the dataset store over HTTPS."""

from urllib.request import Request, urlopen

REQUEST_TIMEOUT_SECONDS = 10


def fetch_csv(dataset: str, *, base_url: str, token: str) -> str:
    """Return the CSV text of ``dataset`` from the store at ``base_url``.

    ``token`` comes from configuration; it is never hardcoded.
    """
    if not base_url.startswith("https://"):
        raise ValueError("Dataset store must use HTTPS")
    url = f"{base_url.rstrip('/')}/datasets/{dataset}.csv"
    request = Request(url)  # noqa: S310
    # Unredirected, so the token is never forwarded if the store redirects.
    request.add_unredirected_header("Authorization", f"Bearer {token}")
    with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:  # noqa: S310
        body: bytes = response.read()
    return body.decode("utf-8")
