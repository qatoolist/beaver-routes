import pytest
from box import Box

from beaver_routes.core.httpx_args_handler import HttpxArgsHandler
from beaver_routes.core.meta import Meta
from beaver_routes.exceptions.exceptions import (
    InvalidHttpMethodError,
    InvalidHttpxArgumentsError,
)


def test_initialization() -> None:
    """Test Meta initialization with parameters and headers.

    This test verifies that the Meta class is properly initialized with
    query parameters and headers.

    Example:
        >>> test_initialization()
    """
    meta = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    assert isinstance(meta.params, Box)
    assert meta.params.q == "search1"
    assert isinstance(meta.headers, Box)
    assert meta.headers.Authorization == "Bearer token1"


def test_set_get_attributes() -> None:
    """Test setting and getting attributes in Meta.

    This test verifies that attributes can be set and retrieved correctly
    in the Meta class.

    Example:
        >>> test_set_get_attributes()
    """
    meta = Meta()
    meta.params.q = "search1"
    assert meta.params.q == "search1"
    meta.json.a.b = "c"
    assert meta.json.a.b == "c"


def test_to_httpx_args() -> None:
    """Test conversion of Meta to httpx request arguments for GET.

    This test verifies that the Meta class can be converted to httpx request
    arguments for a GET request.

    Example:
        >>> test_to_httpx_args()
    """
    meta = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    meta.url = "http://example.com"
    args = HttpxArgsHandler.convert(meta, "GET")
    assert args["params"] == {"q": "search1"}
    assert args["headers"] == {"Authorization": "Bearer token1"}
    assert "cookies" not in args


def test_to_httpx_args_with_post() -> None:
    """Test conversion of Meta to httpx request arguments for POST.

    This test verifies that the Meta class can be converted to httpx request
    arguments for a POST request.

    Example:
        >>> test_to_httpx_args_with_post()
    """
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
    """Test adding two Meta instances.

    This test verifies that two Meta instances can be added together and the
    resulting Meta instance contains the combined attributes.

    Example:
        >>> test_add()
    """
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
    """Test copying a Meta instance.

    This test verifies that a Meta instance can be copied and the copy is
    identical to the original.

    Example:
        >>> test_copy()
    """
    meta1 = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    meta2 = meta1.copy()
    assert meta1.to_dict() == meta2.to_dict()
    meta1.params.q = "new_value"
    assert meta1.params.q != meta2.params.q


def test_repr_str() -> None:
    """Test string representation of Meta.

    This test verifies that the string representations of a Meta instance
    (repr and str) contain the expected attributes.

    Example:
        >>> test_repr_str()
    """
    meta = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    repr_str = repr(meta)
    str_repr = str(meta)
    assert "Meta(params=" in repr_str
    assert '"params":' in str_repr


def test_invalid_http_method() -> None:
    """Test handling of invalid HTTP method.

    This test verifies that an InvalidHttpMethodError is raised when
    an invalid HTTP method is used.

    Example:
        >>> test_invalid_http_method()
    """
    meta = Meta()
    meta.url = "http://example.com"
    with pytest.raises(InvalidHttpMethodError) as exc_info:
        HttpxArgsHandler.convert(meta, "INVALID")
    assert "Invalid HTTP method: INVALID" in str(exc_info.value)


def test_invalid_httpx_arguments() -> None:
    """Test handling of invalid httpx arguments.

    This test verifies that an InvalidHttpxArgumentsError is raised when
    invalid arguments are provided to httpx.

    Example:
        >>> test_invalid_httpx_arguments()
    """
    meta = Meta(params={"q": "search1"}, headers={"Authorization": "Bearer token1"})
    meta.url = "http://example.com"
    with pytest.raises(InvalidHttpxArgumentsError):
        meta.to_httpx_args("INVALID_METHOD")


def test_remove_key() -> None:
    """Test removing a key from Meta.

    This test verifies that a key can be removed from a Meta instance
    and the remaining attributes are unaffected.

    Example:
        >>> test_remove_key()
    """
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
