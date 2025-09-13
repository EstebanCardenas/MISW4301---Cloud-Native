from src.api.http_client import HttpClient
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.internal.post import Post


class PostController:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def get_post(self, post_id: str, auth_token: str) -> Post:
        post = self.http_client.get_post(post_id, auth_token)
        if not post:
            raise ApiException(type=ApiExceptionType.NOT_FOUND, detail="Post not found")
        return post

    def get_route(self, route_id: str, auth_token: str):
        route = self.http_client.get_route(route_id, auth_token)
        if not route:
            raise ApiException(
                type=ApiExceptionType.NOT_FOUND,
                detail="Route not found",
            )
        return route

    def get_offers(self, post_id: str, auth_token: str):
        offers = self.http_client.get_offers(post_id, auth_token)
        if not offers:
            raise ApiException(
                type=ApiExceptionType.NOT_FOUND,
                detail="Offers not found",
            )
        return offers

    def get_score(self, offer_id: str, auth_token: str):
        score = self.http_client.get_score(offer_id, auth_token)
        if not score:
            raise ApiException(
                type=ApiExceptionType.NOT_FOUND,
                detail="Score not found",
            )
        return score

    def get_user_info(self, auth_token: str):
        user_info = self.http_client.get_user_info(auth_token)
        if not user_info:
            raise ApiException(type=ApiExceptionType.NOT_FOUND, detail="User not found")
        return user_info
