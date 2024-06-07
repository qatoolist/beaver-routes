from typing import Any, Dict, Union

# Type aliases for HTTP request components
QueryParams = Union[Dict[str, str], None]
"""Type alias for query parameters in an HTTP request.

Example:
    >>> params: QueryParams = {"q": "search"}
"""

Headers = Union[Dict[str, str], None]
"""Type alias for headers in an HTTP request.

Example:
    >>> headers: Headers = {"Authorization": "Bearer token"}
"""

Cookies = Union[Dict[str, str], None]
"""Type alias for cookies in an HTTP request.

Example:
    >>> cookies: Cookies = {"session_id": "abc123"}
"""

Auth = Union[Any, None]
"""Type alias for authentication information in an HTTP request.

Example:
    >>> auth: Auth = ("username", "password")
"""

Timeout = Union[float, None]
"""Type alias for timeout in an HTTP request.

Example:
    >>> timeout: Timeout = 10.0
"""

ContentType = Union[str, bytes, Dict[str, Any], None]
"""Type alias for content in an HTTP request.

Example:
    >>> content: ContentType = "sample content"
"""

DataType = Union[Dict[str, Any], str, bytes, None]
"""Type alias for data in an HTTP request.

Example:
    >>> data: DataType = {"key": "value"}
"""

FilesType = Union[Dict[str, Union[str, bytes]], None]
"""Type alias for files in an HTTP request.

Example:
    >>> files: FilesType = {"file": ("filename.txt", b"file content")}
"""
