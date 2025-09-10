from uuid import UUID

from src.api.http_client import HttpClient


class UserController:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def get_user_info(self, auth_token: UUID):
        return self.http_client.get_user_info(auth_token)
