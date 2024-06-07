from __future__ import annotations

from http import HTTPStatus
from typing import Any

import httpx
import pytest

from beaver_routes.core.base_route import BaseRoute
from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta
from beaver_routes.exceptions.exceptions import MetaError

# Define hooks for testing


async def route_request_hook(method: str, url: str, meta: Meta) -> None:
    """Example route request hook.

    Args:
        method (str): The HTTP method.
        url (str): The request URL.
        meta (Meta): The request metadata.

    Example:
        >>> await route_request_hook("GET", "http://example.com", Meta())
    """
    print(f"Route request hook: {method} {url} {meta}")
    meta.params.route_hook = "route_hook_value"


async def method_request_hook(method: str, url: str, meta: Meta) -> None:
    """Example method request hook.

    Args:
        method (str): The HTTP method.
        url (str): The request URL.
        meta (Meta): The request metadata.

    Example:
        >>> await method_request_hook("GET", "http://example.com", Meta())
    """
    print(f"Method request hook: {method} {url} {meta}")
    meta.params.method_hook = "method_hook_value"


async def scenario_request_hook(method: str, url: str, meta: Meta) -> None:
    """Example scenario request hook.

    Args:
        method (str): The HTTP method.
        url (str): The request URL.
        meta (Meta): The request metadata.

    Example:
        >>> await scenario_request_hook("GET", "http://example.com", Meta())
    """
    print(f"Scenario request hook: {method} {url} {meta}")
    meta.params.scenario_hook = "scenario_hook_value"


async def route_response_hook(response: httpx.Response) -> None:
    """Example route response hook.

    Args:
        response (httpx.Response): The HTTP response.

    Example:
        >>> await route_response_hook(httpx.Response(status_code=HTTPStatus.OK))
    """
    print(f"Route response hook: {response.status_code}")


async def method_response_hook(response: httpx.Response) -> None:
    """Example method response hook.

    Args:
        response (httpx.Response): The HTTP response.

    Example:
        >>> await method_response_hook(httpx.Response(status_code=HTTPStatus.OK))
    """
    print(f"Method response hook: {response.status_code}")


async def scenario_response_hook(response: httpx.Response) -> None:
    """Example scenario response hook.

    Args:
        response (httpx.Response): The HTTP response.

    Example:
        >>> await scenario_response_hook(httpx.Response(status_code=HTTPStatus.OK))
    """
    print(f"Scenario response hook: {response.status_code}")


class CustomRoute(BaseRoute):
    """Custom route class for testing and demonstration purposes.

    This class demonstrates how to customize a route by overriding the hook and HTTP method
    handlers. It provides examples of adding hooks and setting metadata for various HTTP methods.

    Methods:
        __route__(meta: Meta, hooks: Hook) -> None:
            Customize the route-specific metadata and hooks.
        __get__(meta: Meta, hooks: Hook) -> None:
            Customize the GET-specific metadata and hooks.
        __post__(meta: Meta, hooks: Hook) -> None:
            Customize the POST-specific metadata and hooks.
        __put__(meta: Meta, hooks: Hook) -> None:
            Customize the PUT-specific metadata and hooks.
        __delete__(meta: Meta, hooks: Hook) -> None:
            Customize the DELETE-specific metadata and hooks.
        scenario1(meta: Meta, hooks: Hook) -> None:
            Define a scenario to customize metadata and hooks for testing.
    """

    def __route__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the route-specific metadata and hooks.

        Args:
            meta (Meta): The route metadata.
            hooks (Hook): The route hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__route__(Meta(), Hook())
        """
        hooks.add("request", route_request_hook)
        hooks.add("response", route_response_hook)
        meta.params.route_param = "route_value"

    def __get__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the GET-specific metadata and hooks.

        Args:
            meta (Meta): The GET request metadata.
            hooks (Hook): The GET request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__get__(Meta(), Hook())
        """
        hooks.add("request", method_request_hook)
        hooks.add("response", method_response_hook)
        meta.params.get_param = "get_value"

    def __post__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the POST-specific metadata and hooks.

        Args:
            meta (Meta): The POST request metadata.
            hooks (Hook): The POST request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__post__(Meta(), Hook())
        """
        hooks.add("request", method_request_hook)
        hooks.add("response", method_response_hook)
        meta.params.post_param = "post_value"

    def __put__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the PUT-specific metadata and hooks.

        Args:
            meta (Meta): The PUT request metadata.
            hooks (Hook): The PUT request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__put__(Meta(), Hook())
        """
        hooks.add("request", method_request_hook)
        hooks.add("response", method_response_hook)
        meta.params.put_param = "put_value"

    def __delete__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the DELETE-specific metadata and hooks.

        Args:
            meta (Meta): The DELETE request metadata.
            hooks (Hook): The DELETE request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__delete__(Meta(), Hook())
        """
        hooks.add("request", method_request_hook)
        hooks.add("response", method_response_hook)
        meta.params.delete_param = "delete_value"

    def scenario1(self, meta: Meta, hooks: Hook) -> None:
        """Define a scenario to customize metadata and hooks for testing.

        Args:
            meta (Meta): The scenario metadata.
            hooks (Hook): The scenario hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.scenario1(Meta(), Hook())
        """
        hooks.add("request", scenario_request_hook)
        hooks.add("response", scenario_response_hook)
        meta.params.scenario_param = "scenario_value"


@pytest.fixture  # type: ignore
def mock_httpx_client(monkeypatch: Any) -> None:
    """Fixture to mock httpx.Client and httpx.AsyncClient for testing.

    This fixture replaces the request method of httpx.Client and httpx.AsyncClient
    with a mock implementation that returns a predefined response. This is useful
    for testing purposes to avoid making actual HTTP requests.

    Args:
        monkeypatch (Any): The monkeypatch fixture provided by pytest for modifying attributes.

    Example:
        >>> def test_example(mock_httpx_client):
        ...     response = httpx.get("http://example.com")
        ...     assert response.status_code == HTTPStatus.OK
    """

    class MockResponse:
        """Mock response class to simulate httpx responses.

        Attributes:
            status_code (int): The HTTP status code of the response.
            _json_data (Any): The JSON data to return when calling the json() method.
        """

        def __init__(
            self, status_code: int = HTTPStatus.OK, json_data: Any = None
        ) -> None:
            self.status_code = status_code
            self._json_data = json_data or {}

        def json(self) -> Any:
            """Return the JSON data of the mock response.

            Returns:
                Any: The JSON data of the response.
            """
            return self._json_data

    async def mock_async_request(
        self: Any, method: str, url: str, *, dummy: Any | None = None, **kwargs: Any
    ) -> MockResponse:
        """Mock async request method for httpx.AsyncClient.

        Args:
            self (Any): The instance of the calling object.
            method (str): The HTTP method (e.g., "GET", "POST").
            url (str): The URL for the request.
            dummy (Any | None): A dummy argument for compatibility.
            **kwargs (Any): Additional arguments for the request.

        Returns:
            MockResponse: A mock response object.
        """
        return MockResponse()

    def mock_request(
        self: Any, method: str, url: str, *, dummy: Any | None = None, **kwargs: Any
    ) -> MockResponse:
        """Mock request method for httpx.Client.

        Args:
            self (Any): The instance of the calling object.
            method (str): The HTTP method (e.g., "GET", "POST").
            url (str): The URL for the request.
            dummy (Any | None): A dummy argument for compatibility.
            **kwargs (Any): Additional arguments for the request.

        Returns:
            MockResponse: A mock response object.
        """
        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "request", mock_async_request)
    monkeypatch.setattr(httpx.Client, "request", mock_request)


@pytest.mark.usefixtures("mock_httpx_client")
class TestBaseRoute:
    """Test suite for BaseRoute class.

    This test suite includes tests for initializing routes, handling hooks, and making HTTP requests.
    """

    @pytest.mark.asyncio  # type: ignore
    async def test_route_initialization(self) -> None:
        """Test route initialization.

        This test verifies that the route is initialized with the correct endpoint, meta, and hooks.

        Example:
            >>> test_route_initialization()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        assert route.endpoint == "https://jsonplaceholder.typicode.com/posts/1"
        assert isinstance(route.meta, Meta)
        assert isinstance(route.hooks, Hook)

    @pytest.mark.asyncio  # type: ignore
    async def test_invalid_hook_event(self) -> None:
        """Test handling of invalid hook event.

        This test verifies that a ValueError is raised when adding a hook with an invalid event.

        Example:
            >>> test_invalid_hook_event()
        """
        with pytest.raises(ValueError):
            route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
            route.hooks.add("invalid_event", lambda x: x)

    @pytest.mark.asyncio  # type: ignore
    async def test_no_scenario_func(self) -> None:
        """Test handling of non-existent scenario function.

        This test verifies that an AttributeError is raised when trying to apply a non-existent scenario function.

        Example:
            >>> test_no_scenario_func()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        with pytest.raises(AttributeError):
            await route.for_scenario("non_existent_scenario").async_get()

    @pytest.mark.asyncio  # type: ignore
    async def test_meta_exception(self, monkeypatch: Any) -> None:
        """Test handling of MetaError exception.

        This test verifies that a RuntimeError is raised when a MetaError occurs during request preparation.

        Args:
            monkeypatch (Any): The monkeypatch fixture provided by pytest for modifying attributes.

        Example:
            >>> test_meta_exception(monkeypatch)
        """

        def mock_to_httpx_args_raise(meta: Meta, method: str) -> None:
            raise MetaError("Meta Exception")

        monkeypatch.setattr(Meta, "to_httpx_args", mock_to_httpx_args_raise)

        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        with pytest.raises(RuntimeError, match="Failed to prepare httpx arguments"):
            await route.async_get()

    def test_sync_get(self) -> None:
        """Test synchronous GET request.

        This test verifies that the GET request returns a 200 status code.

        Example:
            >>> test_sync_get()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.get()
        assert response.status_code == HTTPStatus.OK

    def test_sync_post(self) -> None:
        """Test synchronous POST request.

        This test verifies that the POST request returns a 200 status code.

        Example:
            >>> test_sync_post()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.post()
        assert response.status_code == HTTPStatus.OK

    def test_sync_put(self) -> None:
        """Test synchronous PUT request.

        This test verifies that the PUT request returns a 200 status code.

        Example:
            >>> test_sync_put()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.put()
        assert response.status_code == HTTPStatus.OK

    def test_sync_delete(self) -> None:
        """Test synchronous DELETE request.

        This test verifies that the DELETE request returns a 200 status code.

        Example:
            >>> test_sync_delete()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.delete()
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio  # type: ignore
    async def test_async_get(self) -> None:
        """Test asynchronous GET request.

        This test verifies that the GET request returns a 200 status code.

        Example:
            >>> test_async_get()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_get()
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio  # type: ignore
    async def test_async_post(self) -> None:
        """Test asynchronous POST request.

        This test verifies that the POST request returns a 200 status code.

        Example:
            >>> test_async_post()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_post()
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio  # type: ignore
    async def test_async_put(self) -> None:
        """Test asynchronous PUT request.

        This test verifies that the PUT request returns a 200 status code.

        Example:
            >>> test_async_put()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_put()
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio  # type: ignore
    async def test_async_delete(self) -> None:
        """Test asynchronous DELETE request.

        This test verifies that the DELETE request returns a 200 status code.

        Example:
            >>> test_async_delete()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_delete()
        assert response.status_code == HTTPStatus.OK


if __name__ == "__main__":
    pytest.main()
