from http import HTTPStatus


class NotImplementedError(Exception):
    """When some feature are not implemented"""

    def __init__(self) -> None:
        self.response = {"error": type(self).__name__}
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__()

class APIError(Exception):
    """Error handled by api"""

    def __init__(self, status_code: HTTPStatus, response: dict) -> None:
        self.response = {"error": type(self).__name__} | response
        self.status_code = status_code
        super().__init__()


class BadRequestError(APIError):
    """Bad request error"""

    def __init__(self, response: dict) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST, response)


class BodyKeyMissingError(BadRequestError):
    """When a needed key in body is missing"""

    def __init__(self, key_name: str) -> None:
        super().__init__({"key_name": key_name})
class HeaderKeyMissingError(BadRequestError):
    """When a needed key in header is missing"""

    def __init__(self, key_name: str) -> None:
        super().__init__({"key_name": key_name})


class BodyKeyTypeError(BadRequestError):
    """When a type of a body key is wrong"""

    def __init__(self, key_name: str, key_type: type) -> None:
        super().__init__({"key_name": key_name, "type_needed": key_type.__name__})

class HeaderKeyTypeError(BadRequestError):
    """When a type of a header key is wrong"""

    def __init__(self, key_name: str, key_type: type) -> None:
        super().__init__({"key_name": key_name, "type_needed": key_type.__name__})


class UrlParamMissingError(BadRequestError):
    """When a needed param in url is missing"""

    def __init__(self, param_name: str) -> None:
        super().__init__({"param_name": param_name})

class UrlParamTypeError(BadRequestError):
    """When a needed param in url is missing"""

    def __init__(self, param_name: str, param_type: type) -> None:
        super().__init__({"param_name": param_name, "type_needed": param_type.__name__})

class CredentialsError(APIError):
    """When a login error occours"""

    def __init__(self, message: str = "Wrong credentials.") -> None:
        super().__init__(HTTPStatus.NOT_FOUND, {"message": message})

class InvalidTokenError(APIError):
    """When a passed token does not exists"""

    def __init__(self, message: str = "Invalid token.") -> None:
        super().__init__(HTTPStatus.UNAUTHORIZED, {"message": message})

class TimeoutError(APIError):
    """When lost much time in an action"""

    def __init__(self, message: str = "Timeout.") -> None:
        super().__init__(HTTPStatus.REQUEST_TIMEOUT, {"message": message})

class DoNotExistsInDatabaseError(APIError):
    """When something do not exists in database"""

    def __init__(self, table_name: str, message: str | None = None) -> None:
        msg = message or f"Not found on {table_name}"
        super().__init__(HTTPStatus.BAD_REQUEST, {"message": msg})

class AlreadyExistsInDatabaseError(APIError):
    """When something already exists in database"""

    def __init__(self, table_name: str, message: str | None = None) -> None:
        msg = message or f"Already exists in {table_name}"
        super().__init__(HTTPStatus.CONFLICT, {"message": msg})

class UnauthorizedError(APIError):
    """When the acion needs a specific role of something like"""

    def __init__(self, message: str = "Not authorized.") -> None:
        super().__init__(HTTPStatus.UNAUTHORIZED, {"message": message})
