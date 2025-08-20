from enum import Enum


class ApiExceptionType(Enum):
    NOT_FOUND = "not_found"
    INVALID_INPUT = "invalid_input"
    VALIDATION_FAILED = "validation_failed"


class ApiException(Exception):
    def __init__(self, type: ApiExceptionType, detail: str = "An error occurred"):
        self.type = type
        self.detail = detail
