from enum import Enum


class ApiExceptionType(Enum):
    NOT_FOUND = "not_found"
    INVALID_INPUT = "invalid_input"
    VALIDATION_FAILED = "validation_failed"
    UNKNOWN_ERROR = "unknown_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    AUTH_TOKEN_MISSING = "auth_token_missing"  # nosec
    AUTH_TOKEN_INVALID = "auth_token_invalid"  # nosec
    DUPLICATED_RESOURCE = "duplicated_resource"


class ApiException(Exception):
    def __init__(self, type: ApiExceptionType, detail: str = "An error occurred"):
        self.type = type
        self.detail = detail
