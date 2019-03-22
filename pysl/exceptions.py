class APINotInitializedError(Exception):
    """"""

class APIKeyUndefinedError(Exception):
    """1001"""

class APIKeyInvalidError(Exception):
    """1002"""

class APIUnavailableError(Exception):
    """1003"""

class APIKeyInvalidForAPIError(Exception):
    """1004"""

class TooManyRequestsError(Exception):
    """1005 and 1006"""
