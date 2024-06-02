from typing import Any, Callable, Dict, Optional


class BaseMixin:
    def __init__(self, endpoint: str = "") -> None:
        self.scenario_method: Optional[Callable[..., Any]] = None
        self.scenario_groups: Optional[Dict[str, type]] = None
        self.endpoint: str = endpoint
        self._after_hooks: Dict[str, list[Callable[..., Any]]] = {}
        self._request_args: Optional[Dict[str, Any]] = None
        self._response: Optional[Any] = None
        self.current_scenario_group: Optional[str] = None
        self.current_scenario_name: Optional[str] = None
