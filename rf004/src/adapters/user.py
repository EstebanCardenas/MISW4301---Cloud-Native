from src.models.incoming.users import GetUserResponse
from src.models.internal.user import User, UserStatus


def get_user_response_to_internal(user: GetUserResponse) -> User:
    return User(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.fullName,
        dni=user.dni,
        phone_number=user.phoneNumber,
        status=UserStatus(user.status),
    )
