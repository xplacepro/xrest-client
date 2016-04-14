class ApiException(Exception):
    pass


class ValidationError(ApiException):
    pass


class Unauthorized(ApiException):
    pass
