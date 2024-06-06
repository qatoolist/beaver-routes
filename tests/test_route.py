from __future__ import annotations

from typing import Any

import httpx
import pytest

from beaver_routes.core.base_route import BaseRoute
from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta
from beaver_routes.exceptions.exceptions import MetaError


# Define hooks for testing
async def route_request_hook(method: str, url: str, meta: Meta) -> None:
    print(f"Route request hook: {method} {url} {meta}")
    meta.params.route_hook = "route_hook_value"


async def method_request_hook(method: str, url: str, meta: Meta) -> None:
    print(f"Method request hook: {method} {url} {meta}")
    meta.params.method_hook = "method_hook_value"


async def scenario_request_hook(method: str, url: str, meta: Meta) -> None:
    print(f"Scenario request hook: {method} {url} {meta}")
    meta.params.scenario_hook = "scenario_hook_value"


async def route_response_hook(response: httpx.Response) -> None:
    print(f"Route response hook: {response.status_code}")


async def method_response_hook(response: httpx.Response) -> None:
    print(f"Method response hook: {response.status_code}")


async def scenario_response_hook(response: httpx.Response) -> None:
    print(f"Scenario response hook: {response.status_code}")


# CustomRoute for testing
class CustomRoute(BaseRoute):
    def __route__(self, meta: Meta, hooks: Hook) -> None:
        hooks.add("request", route_request_hook)
        hooks.add("response", route_response_hook)
        meta.params.route_param = "route_value"

    def __get__(self, meta: Meta, hooks: Hook) -> None:
        hooks.add("request", method_request_hook)
        hooks.add("response", method_response_hook)
        meta.params.get_param = "get_value"

    def scenario1(self, meta: Meta, hooks: Hook) -> None:
        hooks.add("request", scenario_request_hook)
        hooks.add("response", scenario_response_hook)
        meta.params.scenario_param = "scenario_value"


# Helper function to mock httpx.Client and httpx.AsyncClient
@pytest.fixture  # type: ignore
def mock_httpx_client(monkeypatch) -> None:
    class MockResponse:
        def __init__(self, status_code: int = 200, json_data: Any = None) -> None:
            self.status_code = status_code
            self._json_data = json_data or {}

        def json(self) -> Any:
            return self._json_data

    async def mock_async_request(  # type: ignore
        self, method: str, url: str, **kwargs: Any
    ) -> MockResponse:
        return MockResponse()

    def mock_request(self, method: str, url: str, **kwargs: Any) -> MockResponse:  # type: ignore
        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "request", mock_async_request)
    monkeypatch.setattr(httpx.Client, "request", mock_request)


# Test suite
@pytest.mark.usefixtures("mock_httpx_client")
class TestBaseRoute:
    @pytest.mark.asyncio  # type: ignore
    async def test_route_initialization(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        assert route.endpoint == "https://jsonplaceholder.typicode.com/posts/1"
        assert isinstance(route.meta, Meta)
        assert isinstance(route.hooks, Hook)

    @pytest.mark.asyncio  # type: ignore
    async def test_route_hooks(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.get()

        assert response.status_code == 200
        assert route.meta.params.route_hook == "route_hook_value"
        assert route.meta.params.get_param == "get_value"
        assert route.meta.params.method_hook == "method_hook_value"

    @pytest.mark.asyncio  # type: ignore
    async def test_scenario_hooks(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.for_scenario("scenario1").async_get()

        assert response.status_code == 200
        assert route.meta.params.route_hook == "route_hook_value"
        assert route.meta.params.get_param == "get_value"
        assert route.meta.params.method_hook == "method_hook_value"
        assert route.meta.params.scenario_param == "scenario_value"
        assert route.meta.params.scenario_hook == "scenario_hook_value"

    @pytest.mark.asyncio  # type: ignore
    async def test_invalid_hook_event(self) -> None:
        with pytest.raises(ValueError):
            route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
            route.hooks.add("invalid_event", lambda x: x)

    @pytest.mark.asyncio  # type: ignore
    async def test_no_scenario_func(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        with pytest.raises(AttributeError):
            await route.for_scenario("non_existent_scenario").async_get()

    @pytest.mark.asyncio  # type: ignore
    async def test_meta_exception(self, monkeypatch) -> None:
        def mock_to_httpx_args_raise(meta: Meta, method: str) -> None:
            raise MetaError("Meta Exception")

        monkeypatch.setattr(Meta, "to_httpx_args", mock_to_httpx_args_raise)

        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        with pytest.raises(RuntimeError, match="Failed to prepare httpx arguments"):
            await route.async_get()

    @pytest.mark.asyncio  # type: ignore
    async def test_sync_get(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.get()
        assert response.status_code == 200

    @pytest.mark.asyncio  # type: ignore
    async def test_sync_post(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.post()
        assert response.status_code == 200

    @pytest.mark.asyncio  # type: ignore
    async def test_sync_put(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.put()
        assert response.status_code == 200

    @pytest.mark.asyncio  # type: ignore
    async def test_sync_delete(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.delete()
        assert response.status_code == 200

    @pytest.mark.asyncio  # type: ignore
    async def test_async_get(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_get()
        assert response.status_code == 200

    @pytest.mark.asyncio  # type: ignore
    async def test_async_post(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_post()
        assert response.status_code == 200

    @pytest.mark.asyncio  # type: ignore
    async def test_async_put(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_put()
        assert response.status_code == 200

    @pytest.mark.asyncio  # type: ignore
    async def test_async_delete(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = await route.async_delete()
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
