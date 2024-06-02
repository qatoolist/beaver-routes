from __future__ import annotations

from typing import Any


class AttributeDictionary:
    def __init__(self, data: dict[Any, Any] | None = None):
        self.__dict__["_data"] = {}
        if data:
            for name, value in data.items():
                self._data[name] = self._wrap(value)

    def __getattr__(self, name: str) -> Any:
        if name not in self._data:
            self._data[name] = AttributeDictionary()
        return self._data[name]

    def __setattr__(self, name: str, value: Any) -> None:
        self._data[name] = self._wrap(value)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = self._wrap(value)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def _wrap(self, value: Any) -> Any:
        return AttributeDictionary(value) if isinstance(value, dict) else value

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in self._data.items():
            if key in {"items", "keys"}:
                raise AttributeError(
                    "dictionary conversion not supported for AttributeDictionary with keys 'items' or 'keys'"
                )
            result[key] = (
                value.to_dict() if isinstance(value, AttributeDictionary) else value
            )
        return result

    def __repr__(self) -> str:
        return repr(self._data)

    def __str__(self) -> str:
        return str(self._data)
