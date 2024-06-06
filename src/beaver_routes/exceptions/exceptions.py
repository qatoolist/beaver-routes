class MetaException(Exception):
    """Base exception for Meta-related errors."""

    pass


class AttributeNotFoundError(MetaException):
    """Raised when an attribute is not found in Meta."""

    pass


class InvalidAdditionError(MetaException):
    """Raised when an invalid object is added to Meta."""

    pass


class HttpxArgsHandlerException(Exception):
    """Base exception for HttpxArgsHandler-related errors."""

    pass


class InvalidHttpMethodError(HttpxArgsHandlerException):
    """Raised when an invalid HTTP method is used."""

    pass


class InvalidHttpxArgumentsError(HttpxArgsHandlerException):
    """Raised when invalid arguments are provided to httpx."""

    pass
