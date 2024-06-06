from __future__ import annotations
from typing import Any, Dict, Union
import copy
from box import Box

from beaver_routes.core.httpx_args_handler import HttpxArgsHandler
from beaver_routes._types._types import (
    QueryParams, Headers, Cookies, Auth, Timeout, ContentType, DataType, FilesType
)
from beaver_routes.exceptions.exceptions import InvalidHttpMethodError, InvalidHttpxArgumentsError, MetaException, AttributeNotFoundError, InvalidAdditionError

class Meta:
    def __init__(
        self,
        *,
        params: QueryParams = None,
        headers: Headers = None,
        cookies: Cookies = None,
        auth: Auth = None,
        follow_redirects: Union[bool, None] = None,
        timeout: Timeout = None,
        extensions: Union[Dict[str, Any], None] = None,
        content: ContentType = None,
        data: DataType = None,
        files: FilesType = None,
        json: Any = None,
    ):
        self._attributes = Box(default_box=True)
        self._attributes.params = self._wrap(params) if params is not None else Box(default_box=True)
        self._attributes.headers = self._wrap(headers) if headers is not None else Box(default_box=True)
        self._attributes.cookies = self._wrap(cookies) if cookies is not None else Box(default_box=True)
        self._attributes.auth = auth
        self._attributes.follow_redirects = follow_redirects
        self._attributes.timeout = timeout
        self._attributes.extensions = self._wrap(extensions)
        self._attributes.content = content if content is not None else Box(default_box=True)
        self._attributes.data = self._wrap(data) if data is not None else Box(default_box=True)
        self._attributes.files = self._wrap(files) if files is not None else Box(default_box=True)
        self._attributes.json = self._wrap(json) if json is not None else Box(default_box=True)

    def _wrap(self, value: Any) -> Any:
        return Box(value, default_box=True) if isinstance(value, dict) else value

    def __getattr__(self, name: str) -> Any:
        try:
            return getattr(self._attributes, name)
        except AttributeError:
            raise AttributeNotFoundError(f"Attribute '{name}' not found in Meta")

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_attributes":
            super().__setattr__(name, value)
        else:
            setattr(self._attributes, name, self._wrap(value))

    def to_httpx_args(self, method: str) -> Dict[str, Any]:
        try:
            return HttpxArgsHandler.convert(self, method)
        except InvalidHttpMethodError as e:
            raise InvalidHttpxArgumentsError(f"Failed to convert to httpx args: {e}")
        except Exception as e:
            raise MetaException(f"Failed to convert to httpx args: {e}")

    def __add__(self, other):
        if not isinstance(other, Meta):
            raise InvalidAdditionError("Cannot add non-Meta instance.")

        result = Meta()
        for key, value in self._attributes.items():
            if isinstance(value, Box) and isinstance(other._attributes[key], Box):
                result._attributes[key] = value + other._attributes[key]
            else:
                result._attributes[key] = other._attributes[key] if other._attributes[key] is not None else value
        return result

    def __repr__(self) -> str:
        return f"Meta(params={self._attributes.params}, headers={self._attributes.headers}, cookies={self._attributes.cookies}, auth={self._attributes.auth}, " \
               f"follow_redirects={self._attributes.follow_redirects}, timeout={self._attributes.timeout}, extensions={self._attributes.extensions}, " \
               f"content={self._attributes.content}, data={self._attributes.data}, files={self._attributes.files}, json={self._attributes.json})"

    def __str__(self) -> str:
        return self._dict_to_str(self.to_dict(), indent=4)

    def to_dict(self) -> Dict[str, Any]:
        return self._attributes.to_dict()

    def copy(self) -> Meta:
        copied_meta = Meta()
        copied_meta._attributes = copy.deepcopy(self._attributes)
        return copied_meta

    @staticmethod
    def _dict_to_str(data: Dict[str, Any], indent: int = 0) -> str:
        def custom_repr(value):
            if value is None:
                return 'None'
            elif isinstance(value, dict):
                return Meta._dict_to_str(value, indent=indent + 4)
            return repr(value)
        
        items = []
        for key, value in data.items():
            items.append(f'{" " * indent}"{key}": {custom_repr(value)}')
        
        return "{\n" + ",\n".join(items) + "\n" + " " * indent + "}"
