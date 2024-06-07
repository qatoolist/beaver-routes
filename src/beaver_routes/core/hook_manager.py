from typing import Any

from beaver_routes.core.hook import Hook


class HookManager:
    @staticmethod
    def apply_hooks(hooks: Hook, event: str, *args: Any, **kwargs: Any) -> None:
        hooks.apply_hooks(event, *args, **kwargs)
