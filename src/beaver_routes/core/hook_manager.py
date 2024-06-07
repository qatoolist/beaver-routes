from typing import Any

from beaver_routes.core.hook import Hook


class HookManager:
    """Manager class for applying hooks.

    This class provides a static method to apply hooks to events. It is used to centralize
    the logic of applying request and response hooks for HTTP requests.

    Methods:
        apply_hooks(hooks: Hook, event: str, *args: Any, **kwargs: Any) -> None:
            Apply all hooks for a specified event with provided arguments.
    """

    @staticmethod
    def apply_hooks(hooks: Hook, event: str, *args: Any, **kwargs: Any) -> None:
        """Apply all hooks for a specified event with provided arguments.

        Args:
            hooks (Hook): The Hook object containing request and response hooks.
            event (str): The event for which hooks are applied. Must be "request" or "response".
            *args (Any): Positional arguments to pass to the hook functions.
            **kwargs (Any): Keyword arguments to pass to the hook functions.

        Example:
            >>> def my_request_hook(method, url, meta):
            ...     print(f"Request: {method} {url}")
            >>> hook = Hook()
            >>> hook.add("request", my_request_hook)
            >>> HookManager.apply_hooks(hook, "request", "GET", "http://example.com", {"param": "value"})
        """
        hooks.apply_hooks(event, *args, **kwargs)
