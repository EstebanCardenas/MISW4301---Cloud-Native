import uuid

from src.adapters.user import get_user_response_to_internal
from src.models.incoming.users import GetUserResponse
from src.models.internal.user import UserStatus


def test_types_get_user_response_to_internal() -> None:
    response = GetUserResponse(
        id=uuid.uuid4(),
        username="testuser",
        email="testuser@example.com",
        fullName="Test User",
        dni="12345678",
        phoneNumber="1234567890",
        status="VERIFICADO",
    )

    internal_user = get_user_response_to_internal(response)
    assert isinstance(internal_user.id, uuid.UUID)
    assert isinstance(internal_user.username, str)
    assert isinstance(internal_user.email, str)
    assert isinstance(internal_user.full_name, str)
    assert isinstance(internal_user.dni, str)
    assert isinstance(internal_user.phone_number, str)
    assert isinstance(internal_user.status, UserStatus)


def test_values_get_user_response_to_internal():
    response = GetUserResponse(
        id=uuid.uuid4(),
        username="testuser",
        email="testuser@example.com",
        fullName="Test User",
        dni="12345678",
        phoneNumber="1234567890",
        status="VERIFICADO",
    )

    internal_user = get_user_response_to_internal(response)
    assert internal_user.id == response.id
    assert internal_user.username == response.username
    assert internal_user.email == response.email
    assert internal_user.full_name == response.fullName
    assert internal_user.dni == response.dni
    assert internal_user.phone_number == response.phoneNumber
    assert internal_user.status.value == response.status
