# tests/conftest.py
import pytest
from typing import Any
import httpx


@pytest.fixture  # type: ignore
def mock_httpx_client(monkeypatch) -> None:
    class MockResponse:
        def __init__(self, status_code: int = 200, json_data: Any = None) -> None:
            self.status_code = status_code
            self._json_data = json_data or {}

        def json(self) -> Any:
            return self._json_data

    async def mock_async_request(  # type: ignore
        self, method: str, url: str, *, dummy: Any | None = None, **kwargs: Any
    ) -> MockResponse:
        return MockResponse()

    def mock_request(  # type: ignore
        self, method: str, url: str, *, dummy: Any | None = None, **kwargs: Any
    ) -> MockResponse:
        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "request", mock_async_request)
    monkeypatch.setattr(httpx.Client, "request", mock_request)
