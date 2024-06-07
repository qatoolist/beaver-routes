class MetaError(Exception):
    """Base exception for Meta-related errors.

    This exception is raised for errors related to the Meta class and its operations.
    """

    pass


class AttributeNotFoundError(MetaError):
    """Exception raised when an attribute is not found in Meta.

    This exception is raised when attempting to access an attribute that does not exist
    in the Meta class.

    Example:
        >>> try:
        ...     value = meta.non_existent_attribute
        ... except AttributeNotFoundError as e:
        ...     print(f"Error: {e}")
    """

    pass


class InvalidAdditionError(MetaError):
    """Exception raised when an invalid object is added to Meta.

    This exception is raised when attempting to add a non-Meta instance to a Meta instance.

    Example:
        >>> try:
        ...     result = meta + non_meta_instance
        ... except InvalidAdditionError as e:
        ...     print(f"Error: {e}")
    """

    pass


class HttpxArgsHandlerError(Exception):
    """Base exception for HttpxArgsHandler-related errors.

    This exception is raised for errors related to the HttpxArgsHandler class and its operations.
    """

    pass


class InvalidHttpMethodError(HttpxArgsHandlerError):
    """Exception raised when an invalid HTTP method is used.

    This exception is raised when an unsupported or invalid HTTP method is specified.

    Example:
        >>> try:
        ...     HttpxArgsHandler.convert(meta, "INVALID")
        ... except InvalidHttpMethodError as e:
        ...     print(f"Error: {e}")
    """

    pass


class InvalidHttpxArgumentsError(HttpxArgsHandlerError):
    """Exception raised when invalid arguments are provided to httpx.

    This exception is raised when the arguments provided to the httpx request are invalid
    or improperly formatted.

    Example:
        >>> try:
        ...     HttpxArgsHandler.convert(meta, "GET")
        ... except InvalidHttpxArgumentsError as e:
        ...     print(f"Error: {e}")
    """

    pass
