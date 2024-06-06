from beaver_routes._types.hooks import Hooks


class AfterHooks(Hooks):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)