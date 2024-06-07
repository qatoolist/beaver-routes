# src/beaver_routes/core/scenario_manager.py
from typing import Any

from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta


class ScenarioManager:
    @staticmethod
    def apply_scenario(
        route: Any, scenario_name: str, method_meta: Meta, method_hooks: Hook
    ) -> tuple[Meta, Hook]:
        scenario_meta = method_meta.copy()
        scenario_hooks = method_hooks

        scenario_func = getattr(route, scenario_name)
        scenario_func(scenario_meta, scenario_hooks)

        return scenario_meta, scenario_hooks

    @staticmethod
    def prepare_method_meta_and_hooks(
        route: Any, method: str, route_meta: Meta, route_hooks: Hook
    ) -> tuple[Meta, Hook]:
        method_meta = route_meta.copy()
        method_hooks = route_hooks

        if method == "GET":
            route.__get__(method_meta, method_hooks)
        elif method == "POST":
            route.__post__(method_meta, method_hooks)
        elif method == "PUT":
            route.__put__(method_meta, method_hooks)
        elif method == "DELETE":
            route.__delete__(method_meta, method_hooks)

        return method_meta, method_hooks
