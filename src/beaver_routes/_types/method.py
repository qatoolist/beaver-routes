from typing import Any, Callable, Optional

class Method:
    def __init__(self, func: Optional[Callable[..., Any]] = None):
        self.func = func

    def __call__(self, *args, **kwargs) -> Any:
        if self.func:
            return self.func(*args, **kwargs)
        else:
            raise ValueError("No callable function provided")

    def set_method(self, func: Callable[..., Any]) -> None:
        self.func = func