from __future__ import annotations

from http import HTTPStatus
from typing import Any

import pytest

from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta
from beaver_routes.core.response import Response
from beaver_routes.exceptions.exceptions import MetaError
from tests.custom_route import CustomRoute


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
            >>> await test_route_initialization()
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
            >>> await test_invalid_hook_event()
        """
        with pytest.raises(ValueError):
            route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
            route.hooks.add("invalid_event", lambda x: x)

    @pytest.mark.asyncio  # type: ignore
    async def test_no_scenario_func(self) -> None:
        """Test handling of non-existent scenario function.

        This test verifies that an AttributeError is raised when trying to apply a non-existent scenario function.

        Example:
            >>> await test_no_scenario_func()
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
            >>> await test_meta_exception(monkeypatch)
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
        assert isinstance(response, Response)
        assert response.text == '{"key": "value"}'

    def test_sync_post(self) -> None:
        """Test synchronous POST request.

        This test verifies that the POST request returns a 200 status code.

        Example:
            >>> test_sync_post()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.post()
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response, Response)
        assert response.text == '{"key": "value"}'

    def test_sync_put(self) -> None:
        """Test synchronous PUT request.

        This test verifies that the PUT request returns a 200 status code.

        Example:
            >>> test_sync_put()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.put()
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response, Response)
        assert response.text == '{"key": "value"}'

    def test_sync_delete(self) -> None:
        """Test synchronous DELETE request.

        This test verifies that the DELETE request returns a 200 status code.

        Example:
            >>> test_sync_delete()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.delete()
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response, Response)
        assert response.text == '{"key": "value"}'

    def test_sync_patch(self) -> None:
        """Test synchronous PATCH request.

        This test verifies that the PATCH request returns a 200 status code.

        Example:
            >>> test_sync_patch()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.patch()
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response, Response)
        assert response.text == '{"key": "value"}'

    def test_sync_head(self) -> None:
        """Test synchronous HEAD request.

        This test verifies that the HEAD request returns a 200 status code.

        Example:
            >>> test_sync_head()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.head()
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response, Response)
        assert response.text == '{"key": "value"}'

    def test_sync_options(self) -> None:
        """Test synchronous OPTIONS request.

        This test verifies that the OPTIONS request returns a 200 status code.

        Example:
            >>> test_sync_options()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.options()
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response, Response)
        assert response.text == '{"key": "value"}'

    @pytest.mark.asyncio  # type: ignore
    async def test_async_get(self) -> None:
        """Test asynchronous GET request.

        This test verifies that the GET request returns a 200 status code.

        Example:
            >>> await test_async_get()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_get()
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response, Response)
        assert response.text == '{"key": "value"}'

    @pytest.mark.asyncio  # type: ignore
    async def test_async_post(self) -> None:
        """Test asynchronous POST request.

        This test verifies that the POST request returns a 200 status code.

        Example:
            >>> await test_async_post()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_post()
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio  # type: ignore
    async def test_async_put(self) -> None:
        """Test asynchronous PUT request.

        This test verifies that the PUT request returns a 200 status code.

        Example:
            >>> await test_async_put()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_put()
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio  # type: ignore
    async def test_async_delete(self) -> None:
        """Test asynchronous DELETE request.

        This test verifies that the DELETE request returns a 200 status code.

        Example:
            >>> await test_async_delete()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_delete()
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio  # type: ignore
    async def test_async_patch(self) -> None:
        """Test asynchronous PATCH request.

        This test verifies that the PATCH request returns a 200 status code.

        Example:
            >>> await test_async_patch()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_patch()
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio  # type: ignore
    async def test_async_head(self) -> None:
        """Test asynchronous HEAD request.

        This test verifies that the HEAD request returns a 200 status code.

        Example:
            >>> await test_async_head()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_head()
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio  # type: ignore
    async def test_async_options(self) -> None:
        """Test asynchronous OPTIONS request.

        This test verifies that the OPTIONS request returns a 200 status code.

        Example:
            >>> await test_async_options()
        """
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_options()
        assert response.status_code == HTTPStatus.OK


if __name__ == "__main__":
    pytest.main()
