# Type aliases
from typing import Any, Dict, Union

QueryParams = Union[Dict[str, str], None]
Headers = Union[Dict[str, str], None]
Cookies = Union[Dict[str, str], None]
Auth = Union[Any, None]
Timeout = Union[float, None]
ContentType = Union[str, bytes, Dict[str, Any], None]
DataType = Union[Dict[str, Any], str, bytes, None]
FilesType = Union[Dict[str, Union[str, bytes]], None]
