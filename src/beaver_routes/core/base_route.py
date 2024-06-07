# src/beaver_routes/core/base_route.py

import httpx

from beaver_routes.core.hook import Hook
from beaver_routes.core.hook_manager import HookManager
from beaver_routes.core.http_methods import DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
from beaver_routes.core.meta import Meta
from beaver_routes.core.request_handler import RequestHandler
from beaver_routes.core.scenario_manager import ScenarioManager


class BaseRoute:
    """Base class for defining routes with customizable hooks and metadata.

    This class provides the foundation for creating routes with HTTP methods and hooks
    for request and response handling. It allows defining custom scenarios and
    applying hooks at different stages of the request lifecycle.

    Attributes:
        endpoint (str): The URL endpoint for the route.
        meta (Meta): The metadata associated with the route.
        hooks (Hook): The hooks for request and response handling.
        scenario (str | None): The name of the scenario to be applied.
        request_handler (RequestHandler): The handler for making HTTP requests.
        hook_manager (HookManager): The manager for applying hooks.
        scenario_manager (ScenarioManager): The manager for handling scenarios.

    Methods:
        __route__(self, meta: Meta, hooks: Hook) -> None:
            Customize this method for route-specific meta and hooks.
        __get__(self, meta: Meta, hooks: Hook) -> None:
            Customize this method for GET-specific meta and hooks.
        __post__(self, meta: Meta, hooks: Hook) -> None:
            Customize this method for POST-specific meta and hooks.
        __put__(self, meta: Meta, hooks: Hook) -> None:
            Customize this method for PUT-specific meta and hooks.
        __delete__(self, meta: Meta, hooks: Hook) -> None:
            Customize this method for DELETE-specific meta and hooks.
        __patch__(self, meta: Meta, hooks: Hook) -> None:
            Customize this method for PATCH-specific meta and hooks.
        __head__(self, meta: Meta, hooks: Hook) -> None:
            Customize this method for HEAD-specific meta and hooks.
        __options__(self, meta: Meta, hooks: Hook) -> None:
            Customize this method for OPTIONS-specific meta and hooks.
        for_scenario(self, scenario_name: str) -> "BaseRoute":
            Set the scenario to be applied for the route.
        _invoke(self, method: str) -> httpx.Response:
            Internal method to handle synchronous HTTP requests.
        _async_invoke(self, method: str) -> httpx.Response:
            Internal method to handle asynchronous HTTP requests.
        request(self, method: str) -> httpx.Response:
            Make a synchronous HTTP request with the specified method.
        async_request(self, method: str) -> httpx.Response:
            Make an asynchronous HTTP request with the specified method.
        get(self) -> httpx.Response:
            Make a synchronous GET request.
        async_get(self) -> httpx.Response:
            Make an asynchronous GET request.
        post(self) -> httpx.Response:
            Make a synchronous POST request.
        async_post(self) -> httpx.Response:
            Make an asynchronous POST request.
        put(self) -> httpx.Response:
            Make a synchronous PUT request.
        async_put(self) -> httpx.Response:
            Make an asynchronous PUT request.
        delete(self) -> httpx.Response:
            Make a synchronous DELETE request.
        async_delete(self) -> httpx.Response:
            Make an asynchronous DELETE request.
        patch(self) -> httpx.Response:
            Make a synchronous PATCH request.
        async_patch(self) -> httpx.Response:
            Make an asynchronous PATCH request.
        head(self) -> httpx.Response:
            Make a synchronous HEAD request.
        async_head(self) -> httpx.Response:
            Make an asynchronous HEAD request.
        options(self) -> httpx.Response:
            Make a synchronous OPTIONS request.
        async_options(self) -> httpx.Response:
            Make an asynchronous OPTIONS request.
    """

    def __init__(self, endpoint: str = "") -> None:
        """Initialize the BaseRoute with the given endpoint.

        Args:
            endpoint (str): The URL endpoint for the route. Defaults to an empty string.
        """
        self.endpoint: str = endpoint
        self.meta: Meta = Meta()
        self.hooks: Hook = Hook()
        self.scenario: str | None = None
        self.request_handler = RequestHandler()
        self.hook_manager = HookManager()
        self.scenario_manager = ScenarioManager()

    def __route__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for route-specific meta and hooks.

        Args:
            meta (Meta): The metadata for the route.
            hooks (Hook): The hooks for the route.
        """
        pass

    def __get__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for GET-specific meta and hooks.

        Args:
            meta (Meta): The metadata for the GET request.
            hooks (Hook): The hooks for the GET request.
        """
        raise NotImplementedError("GET method not implemented.")

    def __post__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for POST-specific meta and hooks.

        Args:
            meta (Meta): The metadata for the POST request.
            hooks (Hook): The hooks for the POST request.
        """
        raise NotImplementedError("POST method not implemented.")

    def __put__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for PUT-specific meta and hooks.

        Args:
            meta (Meta): The metadata for the PUT request.
            hooks (Hook): The hooks for the PUT request.
        """
        raise NotImplementedError("PUT method not implemented.")

    def __delete__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for DELETE-specific meta and hooks.

        Args:
            meta (Meta): The metadata for the DELETE request.
            hooks (Hook): The hooks for the DELETE request.
        """
        raise NotImplementedError("DELETE method not implemented.")

    def __patch__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for PATCH-specific meta and hooks.

        Args:
            meta (Meta): The metadata for the PATCH request.
            hooks (Hook): The hooks for the PATCH request.
        """
        raise NotImplementedError("PATCH method not implemented.")

    def __head__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for HEAD-specific meta and hooks.

        Args:
            meta (Meta): The metadata for the HEAD request.
            hooks (Hook): The hooks for the HEAD request.
        """
        raise NotImplementedError("HEAD method not implemented.")

    def __options__(self, meta: Meta, hooks: Hook) -> None:
        """Customize this method for OPTIONS-specific meta and hooks.

        Args:
            meta (Meta): The metadata for the OPTIONS request.
            hooks (Hook): The hooks for the OPTIONS request.
        """
        raise NotImplementedError("OPTIONS method not implemented.")

    def for_scenario(self, scenario_name: str) -> "BaseRoute":
        """Set the scenario to be applied for the route.

        Args:
            scenario_name (str): The name of the scenario to be applied.

        Returns:
            BaseRoute: The instance of the BaseRoute with the scenario set.
        """
        self.scenario = scenario_name
        return self

    def _invoke(self, method: str) -> httpx.Response:
        """Internal method to handle synchronous HTTP requests.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").

        Returns:
            httpx.Response: The HTTP response.
        """
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
        """Internal method to handle asynchronous HTTP requests.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").

        Returns:
            httpx.Response: The HTTP response.
        """
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
        """Make a synchronous HTTP request with the specified method.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").

        Returns:
            httpx.Response: The HTTP response.
        """
        return self._invoke(method)

    async def async_request(self, method: str) -> httpx.Response:
        """Make an asynchronous HTTP request with the specified method.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").

        Returns:
            httpx.Response: The HTTP response.
        """
        return await self._async_invoke(method)

    def get(self) -> httpx.Response:
        """Make a synchronous GET request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = GetUsersRoute()
            >>> response = route.get()
            >>> print(response.json())
        """
        return self.request(GET)

    async def async_get(self) -> httpx.Response:
        """Make an asynchronous GET request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = GetUsersRoute()
            >>> response = await route.async_get()
            >>> print(response.json())
        """
        return await self.async_request(GET)

    def post(self) -> httpx.Response:
        """Make a synchronous POST request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = CreateUserRoute()
            >>> response = route.post()
            >>> print(response.json())
        """
        return self.request(POST)

    async def async_post(self) -> httpx.Response:
        """Make an asynchronous POST request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = CreateUserRoute()
            >>> response = await route.async_post()
            >>> print(response.json())
        """
        return await self.async_request(POST)

    def put(self) -> httpx.Response:
        """Make a synchronous PUT request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = UpdateUserRoute(user_id=2)
            >>> response = route.put()
            >>> print(response.json())
        """
        return self.request(PUT)

    async def async_put(self) -> httpx.Response:
        """Make an asynchronous PUT request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = UpdateUserRoute(user_id=2)
            >>> response = await route.async_put()
            >>> print(response.json())
        """
        return await self.async_request(PUT)

    def delete(self) -> httpx.Response:
        """Make a synchronous DELETE request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = DeleteUserRoute(user_id=2)
            >>> response = route.delete()
            >>> print(response.status_code)
        """
        return self.request(DELETE)

    async def async_delete(self) -> httpx.Response:
        """Make an asynchronous DELETE request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = DeleteUserRoute(user_id=2)
            >>> response = await route.async_delete()
            >>> print(response.status_code)
        """
        return await self.async_request(DELETE)

    def patch(self) -> httpx.Response:
        """Make a synchronous PATCH request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = PatchUserRoute(user_id=2)
            >>> response = route.patch()
            >>> print(response.json())
        """
        return self.request(PATCH)

    async def async_patch(self) -> httpx.Response:
        """Make an asynchronous PATCH request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = PatchUserRoute(user_id=2)
            >>> response = await route.async_patch()
            >>> print(response.json())
        """
        return await self.async_request(PATCH)

    def head(self) -> httpx.Response:
        """Make a synchronous HEAD request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = HeadUserRoute(user_id=2)
            >>> response = route.head()
            >>> print(response.status_code)
        """
        return self.request(HEAD)

    async def async_head(self) -> httpx.Response:
        """Make an asynchronous HEAD request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = HeadUserRoute(user_id=2)
            >>> response = await route.async_head()
            >>> print(response.status_code)
        """
        return await self.async_request(HEAD)

    def options(self) -> httpx.Response:
        """Make a synchronous OPTIONS request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = OptionsUserRoute(user_id=2)
            >>> response = route.options()
            >>> print(response.status_code)
        """
        return self.request(OPTIONS)

    async def async_options(self) -> httpx.Response:
        """Make an asynchronous OPTIONS request.

        Returns:
            httpx.Response: The HTTP response.

        Example:
            >>> route = OptionsUserRoute(user_id=2)
            >>> response = await route.async_options()
            >>> print(response.status_code)
        """
        return await self.async_request(OPTIONS)
