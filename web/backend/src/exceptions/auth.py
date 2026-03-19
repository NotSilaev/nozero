class UnauthorizedError(Exception):
    """The client is not authorized."""
    pass


class AlreadyAuthorizedError(Exception):
    """The client is already authorized."""
    pass
