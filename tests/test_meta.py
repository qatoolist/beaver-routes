import pytest
from box import Box

from beaver_routes.core.httpx_args_handler import HttpxArgsHandler
from beaver_routes.core.meta import Meta
from beaver_routes.exceptions.exceptions import (
    InvalidHttpMethodError,
    InvalidHttpxArgumentsError,
)


def test_initialization() -> None:
    meta = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    assert isinstance(meta.params, Box)
    assert meta.params.q == "search1"
    assert isinstance(meta.headers, Box)
    assert meta.headers.Authorization == "Bearer token1"


def test_set_get_attributes() -> None:
    meta = Meta()
    meta.params.q = "search1"
    assert meta.params.q == "search1"
    meta.json.a.b = "c"
    assert meta.json.a.b == "c"


def test_to_httpx_args() -> None:
    meta = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    meta.url = "http://example.com"
    args = HttpxArgsHandler.convert(meta, "GET")
    assert args["params"] == {"q": "search1"}
    assert args["headers"] == {"Authorization": "Bearer token1"}
    assert "cookies" not in args


def test_to_httpx_args_with_post() -> None:
    meta = Meta(
        params={"q": "search1"},
        headers={"Authorization": "Bearer token1"},
        data={"key": "value"},
    )
    meta.url = "http://example.com"
    args = HttpxArgsHandler.convert(meta, "POST")
    assert args["params"] == {"q": "search1"}
    assert args["headers"] == {"Authorization": "Bearer token1"}
    assert args["data"] == {"key": "value"}
    assert "cookies" not in args


def test_add() -> None:
    meta1 = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    meta2 = Meta(
        params={"page": "2"}, headers={"User-Agent": "my-app"}, json={"key": "value"}
    )
    meta3 = meta1 + meta2
    assert meta3.params.q == "search1"
    assert meta3.params.page == "2"
    assert meta3.headers.Authorization == "Bearer token1"
    assert meta3.headers["User-Agent"] == "my-app"
    assert meta3.json.key == "value"


def test_copy() -> None:
    meta1 = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    meta2 = meta1.copy()
    assert meta1.to_dict() == meta2.to_dict()
    meta1.params.q = "new_value"
    assert meta1.params.q != meta2.params.q


def test_repr_str() -> None:
    meta = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    repr_str = repr(meta)
    str_repr = str(meta)
    assert "Meta(params=" in repr_str
    assert '"params":' in str_repr


def test_invalid_http_method() -> None:
    # Initialize a Meta object with default parameters
    meta = Meta()
    meta.url = "http://example.com"  # Setting the URL as part of the test setup
    with pytest.raises(InvalidHttpMethodError) as exc_info:
        # Attempt to convert Meta object with an invalid HTTP method
        HttpxArgsHandler.convert(meta, "INVALID")
    # Check if the correct exception message is captured
    assert "Invalid HTTP method: INVALID" in str(exc_info.value)


def test_invalid_httpx_arguments() -> None:
    meta = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    meta.url = "http://example.com"
    with pytest.raises(InvalidHttpxArgumentsError):
        meta.to_httpx_args("INVALID_METHOD")


def test_remove_key() -> None:
    meta = Meta()
    meta.json = {"a": {"b": {"c": "d", "e": "f"}, "x": "y", "z": "z"}}

    # Remove the 'x': 'y' key-value pair
    del meta.json.a.x  # type: ignore

    # Verify the key-value pair has been removed
    assert "x" not in meta.json.a  # type: ignore
    assert meta.json.a.z == "z"  # type: ignore
    assert meta.json.a.b.c == "d"  # type: ignore
    assert meta.json.a.b.e == "f"  # type: ignore


if __name__ == "__main__":
    pytest.main()
