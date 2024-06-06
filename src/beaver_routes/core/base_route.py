from typing import Any, Optional, Callable
import httpx
from box import Box
from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta

class BaseRoute:
    def __init__(self, endpoint: str = ''):
        self.endpoint = endpoint
        self.meta = Meta()
        self.hooks = Hook()
        self.scenario = None

    def __route__(self, meta: Meta, hooks: Hook):
        """Customize this method for route-specific meta and hooks."""
        pass

    def __get__(self, meta: Meta, hooks: Hook):
        """Customize this method for GET-specific meta and hooks."""
        pass

    def __post__(self, meta: Meta, hooks: Hook):
        """Customize this method for POST-specific meta and hooks."""
        pass

    def __put__(self, meta: Meta, hooks: Hook):
        """Customize this method for PUT-specific meta and hooks."""
        pass

    def __delete__(self, meta: Meta, hooks: Hook):
        """Customize this method for DELETE-specific meta and hooks."""
        pass

    def for_scenario(self, scenario_name: str) -> 'BaseRoute':
        self.scenario = scenario_name
        return self

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        with httpx.Client() as client:
            return client.request(method, url, **kwargs)

    async def _async_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.request(method, url, **kwargs)

    def _invoke(self, method: str) -> httpx.Response:
        route_meta = self.meta.copy()
        route_hooks = Hook()

        self.__route__(route_meta, route_hooks)

        method_meta = route_meta.copy()
        method_hooks = route_hooks

        if method == "GET":
            self.__get__(method_meta, method_hooks)
        elif method == "POST":
            self.__post__(method_meta, method_hooks)
        elif method == "PUT":
            self.__put__(method_meta, method_hooks)
        elif method == "DELETE":
            self.__delete__(method_meta, method_hooks)

        final_meta = method_meta
        final_hooks = method_hooks

        if self.scenario:
            scenario_meta = method_meta.copy()
            scenario_hooks = method_hooks

            scenario_func = getattr(self, self.scenario)
            scenario_func(scenario_meta, scenario_hooks)

            final_meta = scenario_meta
            final_hooks = scenario_hooks

        final_hooks.apply_hooks('request', method, self.endpoint, final_meta)

        url = self.endpoint

        try:
            httpx_args = final_meta.to_httpx_args(method)
        except Exception as e:
            raise RuntimeError(f"Failed to prepare httpx arguments: {e}")

        response = self._request(method, url, **httpx_args)

        final_hooks.apply_hooks('response', response)

        return response

    async def _async_invoke(self, method: str) -> httpx.Response:
        route_meta = self.meta.copy()
        route_hooks = Hook()

        self.__route__(route_meta, route_hooks)

        method_meta = route_meta.copy()
        method_hooks = route_hooks

        if method == "GET":
            self.__get__(method_meta, method_hooks)
        elif method == "POST":
            self.__post__(method_meta, method_hooks)
        elif method == "PUT":
            self.__put__(method_meta, method_hooks)
        elif method == "DELETE":
            self.__delete__(method_meta, method_hooks)

        final_meta = method_meta
        final_hooks = method_hooks

        if self.scenario:
            scenario_meta = method_meta.copy()
            scenario_hooks = method_hooks

            scenario_func = getattr(self, self.scenario)
            scenario_func(scenario_meta, scenario_hooks)

            final_meta = scenario_meta
            final_hooks = scenario_hooks

        final_hooks.apply_hooks('request', method, self.endpoint, final_meta)

        url = self.endpoint

        try:
            httpx_args = final_meta.to_httpx_args(method)
        except Exception as e:
            raise RuntimeError(f"Failed to prepare httpx arguments: {e}")

        response = await self._async_request(method, url, **httpx_args)

        final_hooks.apply_hooks('response', response)

        return response

    def get(self) -> httpx.Response:
        return self._invoke("GET")

    async def async_get(self) -> httpx.Response:
        return await self._async_invoke("GET")

    def post(self) -> httpx.Response:
        return self._invoke("POST")

    async def async_post(self) -> httpx.Response:
        return await self._async_invoke("POST")

    def put(self) -> httpx.Response:
        return self._invoke("PUT")

    async def async_put(self) -> httpx.Response:
        return await self._async_invoke("PUT")

    def delete(self) -> httpx.Response:
        return self._invoke("DELETE")

    async def async_delete(self) -> httpx.Response:
        return await self._async_invoke("DELETE")
