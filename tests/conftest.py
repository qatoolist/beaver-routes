from http import HTTPStatus
from typing import Any

import httpx
import pytest

from beaver_routes.core.response import Response


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
            self,
            status_code: int = HTTPStatus.OK,
            json_data: Any = None,
            content: bytes = b"",
            text: str = '{"key": "value"}',
            cookies: dict[Any, Any] | None = {"session_id": "abc123"},
        ) -> None:
            self.status_code = status_code
            self._json_data = json_data or {}
            self.content = content
            self.text = text
            self.cookies = cookies

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


@pytest.fixture  # type: ignore
def httpx_response() -> httpx.Response:
    """Fixture for creating a mock HTTPX response."""
    response = httpx.Response(
        status_code=200,
        headers={"content-type": "application/json"},
        content=b'{"key": "value"}',
        request=httpx.Request("GET", "https://example.com"),
    )
    # Manually set cookies if needed
    response.cookies["session_id"] = "abc123"
    return response


@pytest.fixture  # type: ignore
def response(httpx_response: Any) -> Response:
    """Fixture for creating a beaver-routes Response."""
    return Response(httpx_response)
