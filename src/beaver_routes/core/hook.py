from typing import Any, Callable, List


class Hook:
    """Class for managing request and response hooks.

    This class provides functionality to add and apply hooks for HTTP requests and responses.
    Hooks are functions that are executed at specific points in the request-response lifecycle.

    Attributes:
        request_hooks (List[Callable[..., Any]]): List of hooks for requests.
        response_hooks (List[Callable[..., Any]]): List of hooks for responses.

    Methods:
        add(event: str, hook_func: Callable[..., Any]) -> None:
            Add a hook function for a specified event (request or response).
        apply_hooks(event: str, *args: Any, **kwargs: Any) -> None:
            Apply all hooks for a specified event with provided arguments.
    """

    def __init__(self) -> None:
        """Initialize the Hook object with empty hook lists."""
        self.request_hooks: List[Callable[..., Any]] = []
        self.response_hooks: List[Callable[..., Any]] = []

    def add(self, event: str, hook_func: Callable[..., Any]) -> None:
        """Add a hook function for a specified event.

        Args:
            event (str): The event for which the hook function is added. Must be "request" or "response".
            hook_func (Callable[..., Any]): The hook function to add.

        Raises:
            ValueError: If the event is not "request" or "response".

        Example:
            >>> def my_request_hook(*args, **kwargs):
            ...     print("Request hook executed")
            >>> hook = Hook()
            >>> hook.add("request", my_request_hook)
        """
        if event == "request":
            self.request_hooks.append(hook_func)
        elif event == "response":
            self.response_hooks.append(hook_func)
        else:
            raise ValueError("Event must be 'request' or 'response'")

    def apply_hooks(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Apply all hooks for a specified event with provided arguments.

        Args:
            event (str): The event for which hooks are applied. Must be "request" or "response".
            *args (Any): Positional arguments to pass to the hook functions.
            **kwargs (Any): Keyword arguments to pass to the hook functions.

        Raises:
            ValueError: If the event is not "request" or "response".

        Example:
            >>> def my_request_hook(method, url, meta):
            ...     print(f"Request: {method} {url}")
            >>> hook = Hook()
            >>> hook.add("request", my_request_hook)
            >>> hook.apply_hooks("request", "GET", "http://example.com", {"param": "value"})
        """
        if event == "request":
            for hook in self.request_hooks:
                hook(*args, **kwargs)
        elif event == "response":
            for hook in self.response_hooks:
                hook(*args, **kwargs)
        else:
            raise ValueError("Event must be 'request' or 'response'")
