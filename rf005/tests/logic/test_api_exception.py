from src.exceptions.api_exception import ApiException, ApiExceptionType


def test_api_exception_type_and_detail_defaults():
    exc = ApiException(ApiExceptionType.NOT_FOUND)
    assert exc.type == ApiExceptionType.NOT_FOUND
    assert exc.detail == "An error occurred"


def test_api_exception_custom_detail():
    msg = "Recurso no encontrado"
    exc = ApiException(ApiExceptionType.NOT_FOUND, msg)
    assert exc.type == ApiExceptionType.NOT_FOUND
    assert exc.detail == msg


def test_api_exception_types_enum_values():
    # Ensure enum contains all expected members
    members = {
        "NOT_FOUND",
        "INVALID_INPUT",
        "VALIDATION_FAILED",
        "UNKNOWN_ERROR",
        "SERVICE_UNAVAILABLE",
        "AUTH_TOKEN_MISSING",
        "AUTH_TOKEN_EXPIRED",
    }
    assert set(ApiExceptionType.__members__.keys()) == members


def test_api_exception_is_exception_subclass():
    exc = ApiException(ApiExceptionType.UNKNOWN_ERROR, "boom")
    assert isinstance(exc, Exception)
    assert isinstance(exc, ApiException)
