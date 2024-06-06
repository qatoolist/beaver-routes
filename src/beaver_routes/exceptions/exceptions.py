class MetaError(Exception):
    """Base exception for Meta-related errors."""

    pass


class AttributeNotFoundError(MetaError):
    """Raised when an attribute is not found in Meta."""

    pass


class InvalidAdditionError(MetaError):
    """Raised when an invalid object is added to Meta."""

    pass


class HttpxArgsHandlerError(Exception):
    """Base exception for HttpxArgsHandler-related errors."""

    pass


class InvalidHttpMethodError(HttpxArgsHandlerError):
    """Raised when an invalid HTTP method is used."""

    pass


class InvalidHttpxArgumentsError(HttpxArgsHandlerError):
    """Raised when invalid arguments are provided to httpx."""

    pass
