from typing import Any, Callable, Optional

from beaver_routes._types.method import Method


class ScenarioMethod(Method):
    def __init__(self, func: Optional[Callable[..., Any]] = None):
        super().__init__(func)
