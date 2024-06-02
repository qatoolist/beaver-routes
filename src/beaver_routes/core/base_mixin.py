from typing import Any, Callable

import requests


class BaseMixin:
    def __init__(self, endpoint: str = "") -> None:
        self.scenario_method: Callable = None
        self.scenario_groups: map[str, type] = None
        self.endpoint: str = endpoint
        self._after_hooks: dict[str, list[Callable]] = {}
        self._request_args: dict[str, Any] = None
        self._response: requests.Response | None = None
        self.current_scenario_group: str | None = None
        self.current_scenario_name: str | None = None
