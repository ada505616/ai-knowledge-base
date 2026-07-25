"""Utilities for retrieving repository metadata from the GitHub API."""

import json
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen


def get_repository_info(
    owner: str,
    repository: str,
    token: str | None = None,
    timeout: float = 10.0,
) -> dict[str, Any]:
    """Fetch basic metadata for a GitHub repository.

    Args:
        owner: GitHub account or organization that owns the repository.
        repository: Name of the repository.
        token: Optional GitHub personal access token for authenticated requests.
        timeout: Maximum number of seconds to wait for the API response.

    Returns:
        A dictionary containing ``stars``, ``forks``, and ``description``.

    Raises:
        ValueError: If ``owner`` or ``repository`` is empty.
        urllib.error.HTTPError: If GitHub rejects the request or the repository
            does not exist.
        urllib.error.URLError: If the GitHub API cannot be reached.
    """
    if not owner or not repository:
        raise ValueError("owner and repository must not be empty")

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-knowledge-base",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    encoded_owner = quote(owner, safe="")
    encoded_repository = quote(repository, safe="")
    url = f"https://api.github.com/repos/{encoded_owner}/{encoded_repository}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        data = json.load(response)

    return {
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "description": data["description"],
    }
