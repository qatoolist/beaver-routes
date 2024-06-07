from typing import Any, Callable

from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta


class ScenarioManager:
    """Manager class for handling scenarios.

    This class provides static methods to apply scenarios and prepare metadata and hooks
    for HTTP methods. It is used to manage the specific logic for scenarios within routes.

    Methods:
        apply_scenario(route: Any, scenario_name: str, method_meta: Meta, method_hooks: Hook) -> tuple[Meta, Hook]:
            Apply a scenario to the given method metadata and hooks.
        prepare_method_meta_and_hooks(route: Any, method: str, route_meta: Meta, route_hooks: Hook) -> tuple[Meta, Hook]:
            Prepare metadata and hooks for the specified HTTP method.
    """

    method_map: dict[str, Callable[[Any, Meta, Hook], None]] = {
        "GET": lambda route, meta, hooks: route.__get__(meta, hooks),
        "POST": lambda route, meta, hooks: route.__post__(meta, hooks),
        "PUT": lambda route, meta, hooks: route.__put__(meta, hooks),
        "DELETE": lambda route, meta, hooks: route.__delete__(meta, hooks),
        "PATCH": lambda route, meta, hooks: route.__patch__(meta, hooks),
        "HEAD": lambda route, meta, hooks: route.__head__(meta, hooks),
        "OPTIONS": lambda route, meta, hooks: route.__options__(meta, hooks),
    }

    @staticmethod
    def apply_scenario(
        route: Any, scenario_name: str, method_meta: Meta, method_hooks: Hook
    ) -> tuple[Meta, Hook]:
        """Apply a scenario to the given method metadata and hooks.

        Args:
            route (Any): The route object containing the scenario.
            scenario_name (str): The name of the scenario to apply.
            method_meta (Meta): The method metadata.
            method_hooks (Hook): The method hooks.

        Returns:
            tuple[Meta, Hook]: The updated metadata and hooks after applying the scenario.

        Example:
            >>> class MyRoute:
            ...     def scenario1(self, meta, hooks):
            ...         meta.params['scenario'] = 'scenario1'
            >>> route = MyRoute()
            >>> meta = Meta()
            >>> hooks = Hook()
            >>> ScenarioManager.apply_scenario(route, 'scenario1', meta, hooks)
            (Meta(params={'scenario': 'scenario1'}), Hook())
        """
        scenario_meta = method_meta.copy()
        scenario_hooks = method_hooks

        scenario_func = getattr(route, scenario_name)
        scenario_func(scenario_meta, scenario_hooks)

        return scenario_meta, scenario_hooks

    @staticmethod
    def prepare_method_meta_and_hooks(
        route: Any, method: str, route_meta: Meta, route_hooks: Hook
    ) -> tuple[Meta, Hook]:
        """Prepare metadata and hooks for the specified HTTP method.

        Args:
            route (Any): The route object containing the method.
            method (str): The HTTP method (e.g., "GET", "POST").
            route_meta (Meta): The route metadata.
            route_hooks (Hook): The route hooks.

        Returns:
            tuple[Meta, Hook]: The prepared metadata and hooks for the method.

        Example:
            >>> class MyRoute:
            ...     def __get__(self, meta, hooks):
            ...         meta.params['method'] = 'GET'
            >>> route = MyRoute()
            >>> meta = Meta()
            >>> hooks = Hook()
            >>> ScenarioManager.prepare_method_meta_and_hooks(route, 'GET', meta, hooks)
            (Meta(params={'method': 'GET'}), Hook())
        """
        method_meta = route_meta.copy()
        method_hooks = route_hooks

        if method in ScenarioManager.method_map:
            ScenarioManager.method_map[method](route, method_meta, method_hooks)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return method_meta, method_hooks
