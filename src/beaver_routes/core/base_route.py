# src/beaver_routes/core/base_route.py

import httpx

from beaver_routes.core.hook import Hook
from beaver_routes.core.hook_manager import HookManager
from beaver_routes.core.meta import Meta
from beaver_routes.core.request_handler import RequestHandler
from beaver_routes.core.scenario_manager import ScenarioManager


class BaseRoute:
    def __init__(self, endpoint: str = "") -> None:
        self.endpoint: str = endpoint
        self.meta: Meta = Meta()
        self.hooks: Hook = Hook()
        self.scenario: str | None = None
        self.request_handler = RequestHandler()
        self.hook_manager = HookManager()
        self.scenario_manager = ScenarioManager()

    def __route__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for route-specific meta and hooks."""
        pass

    def __get__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for GET-specific meta and hooks."""
        raise NotImplementedError("GET method not implemented.")

    def __post__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for POST-specific meta and hooks."""
        raise NotImplementedError("POST method not implemented.")

    def __put__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for PUT-specific meta and hooks."""
        raise NotImplementedError("PUT method not implemented.")

    def __delete__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for DELETE-specific meta and hooks."""
        raise NotImplementedError("DELETE method not implemented.")

    def for_scenario(self, scenario_name: str) -> "BaseRoute":
        self.scenario = scenario_name
        return self

    def _invoke(self, method: str) -> httpx.Response:
        route_meta = self.meta.copy()
        route_hooks = Hook()

        self.__route__(route_meta, route_hooks)
        method_meta, method_hooks = self.scenario_manager.prepare_method_meta_and_hooks(
            self, method, route_meta, route_hooks
        )

        if self.scenario:
            method_meta, method_hooks = self.scenario_manager.apply_scenario(
                self, self.scenario, method_meta, method_hooks
            )

        self.hook_manager.apply_hooks(
            method_hooks, "request", method, self.endpoint, method_meta
        )

        url = self.endpoint
        try:
            httpx_args = method_meta.to_httpx_args(method)
        except Exception as e:
            raise RuntimeError(f"Failed to prepare httpx arguments: {e}")

        response = self.request_handler.sync_request(method, url, **httpx_args)

        self.hook_manager.apply_hooks(method_hooks, "response", response)

        return response

    async def _async_invoke(self, method: str) -> httpx.Response:
        route_meta = self.meta.copy()
        route_hooks = Hook()

        self.__route__(route_meta, route_hooks)
        method_meta, method_hooks = self.scenario_manager.prepare_method_meta_and_hooks(
            self, method, route_meta, route_hooks
        )

        if self.scenario:
            method_meta, method_hooks = self.scenario_manager.apply_scenario(
                self, self.scenario, method_meta, method_hooks
            )

        self.hook_manager.apply_hooks(
            method_hooks, "request", method, self.endpoint, method_meta
        )

        url = self.endpoint
        try:
            httpx_args = method_meta.to_httpx_args(method)
        except Exception as e:
            raise RuntimeError(f"Failed to prepare httpx arguments: {e}")

        response = await self.request_handler.async_request(method, url, **httpx_args)

        self.hook_manager.apply_hooks(method_hooks, "response", response)

        return response

    def request(self, method: str) -> httpx.Response:
        return self._invoke(method)

    async def async_request(self, method: str) -> httpx.Response:
        return await self._async_invoke(method)

    def get(self) -> httpx.Response:
        return self.request("GET")

    async def async_get(self) -> httpx.Response:
        return await self.async_request("GET")

    def post(self) -> httpx.Response:
        return self.request("POST")

    async def async_post(self) -> httpx.Response:
        return await self.async_request("POST")

    def put(self) -> httpx.Response:
        return self.request("PUT")

    async def async_put(self) -> httpx.Response:
        return await self.async_request("PUT")

    def delete(self) -> httpx.Response:
        return self.request("DELETE")

    async def async_delete(self) -> httpx.Response:
        return await self.async_request("DELETE")
