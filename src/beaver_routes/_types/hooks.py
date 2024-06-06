from typing import Any, Callable

from beaver_routes._types.method import Method

class Hooks(dict[str, list[Method]]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_hook(self, name: str, hook: Callable[..., Any]) -> None:
        method = Method(hook)
        if name not in self:
            self[name] = []
        self[name].append(method)
