from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class BettingApiClient:
    """Small API client used by both API and UI tests for stable setup."""

    base_url: str
    user_id: str

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"x-user-id": self.user_id})

    def get_matches(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/matches")

    def get_balance(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/balance")

    def reset_balance(self) -> requests.Response:
        return self.session.post(f"{self.base_url}/api/reset-balance")

    def place_bet(self, payload: dict[str, Any], *, include_user_header: bool = True) -> requests.Response:
        headers = None
        if not include_user_header:
            headers = {"x-user-id": ""}
        return self.session.post(f"{self.base_url}/api/place-bet", json=payload, headers=headers)
