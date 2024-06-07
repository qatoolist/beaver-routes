# src/beaver_routes/core/custom_route.py
from beaver_routes.core.base_route import BaseRoute
from beaver_routes.core.meta import Meta
from beaver_routes.core.hook import Hook
from .hooks_for_testing import (
    route_request_hook,
    method_request_hook,
    scenario_request_hook,
    route_response_hook,
    method_response_hook,
    scenario_response_hook,
)


class CustomRoute(BaseRoute):
    def __route__(self, meta: Meta, hooks: Hook) -> None:
        hooks.add("request", route_request_hook)
        hooks.add("response", route_response_hook)
        meta.params.route_param = "route_value"

    def __get__(self, meta: Meta, hooks: Hook) -> None:
        hooks.add("request", method_request_hook)
        hooks.add("response", method_response_hook)
        meta.params.get_param = "get_value"

    def __post__(self, meta: Meta, hooks: Hook) -> None:
        hooks.add("request", method_request_hook)
        hooks.add("response", method_response_hook)
        meta.params.post_param = "post_value"

    def __put__(self, meta: Meta, hooks: Hook) -> None:
        hooks.add("request", method_request_hook)
        hooks.add("response", method_response_hook)
        meta.params.put_param = "put_value"

    def __delete__(self, meta: Meta, hooks: Hook) -> None:
        hooks.add("request", method_request_hook)
        hooks.add("response", method_response_hook)
        meta.params.delete_param = "delete_value"

    def scenario1(self, meta: Meta, hooks: Hook) -> None:
        hooks.add("request", scenario_request_hook)
        hooks.add("response", scenario_response_hook)
        meta.params.scenario_param = "scenario_value"

