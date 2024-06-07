# tests/test_route.py
import pytest

from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta
from beaver_routes.exceptions.exceptions import MetaError

from .custom_route import CustomRoute


@pytest.mark.usefixtures("mock_httpx_client")
class TestBaseRoute:
    @pytest.mark.asyncio  # type: ignore
    async def test_route_initialization(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        assert route.endpoint == "https://jsonplaceholder.typicode.com/posts/1"
        assert isinstance(route.meta, Meta)
        assert isinstance(route.hooks, Hook)

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

    def test_sync_get(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.get()
        assert response.status_code == 200

    def test_sync_post(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.post()
        assert response.status_code == 200

    def test_sync_put(self) -> None:
        route = CustomRoute("https://jsonplaceholder.typicode.com/posts/1")
        response = route.put()
        assert response.status_code == 200

    def test_sync_delete(self) -> None:
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
