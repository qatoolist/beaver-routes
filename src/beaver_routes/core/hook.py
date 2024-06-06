from typing import Callable, List

class Hook:
    def __init__(self):
        self.request_hooks: List[Callable] = []
        self.response_hooks: List[Callable] = []

    def add(self, event: str, hook_func: Callable):
        if event == 'request':
            self.request_hooks.append(hook_func)
        elif event == 'response':
            self.response_hooks.append(hook_func)
        else:
            raise ValueError("Event must be 'request' or 'response'")

    def apply_hooks(self, event: str, *args, **kwargs):
        if event == 'request':
            for hook in self.request_hooks:
                hook(*args, **kwargs)
        elif event == 'response':
            for hook in self.response_hooks:
                hook(*args, **kwargs)
        else:
            raise ValueError("Event must be 'request' or 'response'")
