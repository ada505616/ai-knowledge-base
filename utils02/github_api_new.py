"""GitHub repository metadata client."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def get_repository_info(
    owner: str,
    repository: str,
    token: str | None = None,
    timeout: float = 10,
) -> dict[str, Any]:
    """Return the star count, fork count, and description for a repository.

    Args:
        owner: GitHub account or organization name.
        repository: Repository name.
        token: Optional GitHub personal access token for authenticated requests.
        timeout: Request timeout in seconds.

    Raises:
        ValueError: If the repository does not exist or access is denied.
        RuntimeError: If the GitHub API request fails for another reason.
    """
    url = f"https://api.github.com/repos/{owner}/{repository}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-repository-info-client",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        with urlopen(Request(url, headers=headers), timeout=timeout) as response:
            payload = json.load(response)
    except HTTPError as error:
        if error.code in (401, 403, 404):
            raise ValueError(
                f"无法获取仓库 {owner}/{repository}（GitHub API 状态码：{error.code}）"
            ) from error
        raise RuntimeError(f"GitHub API 请求失败（状态码：{error.code}）") from error
    except URLError as error:
        raise RuntimeError("无法连接 GitHub API") from error

    return {
        "stars": payload["stargazers_count"],
        "forks": payload["forks_count"],
        "description": payload["description"],
    }
