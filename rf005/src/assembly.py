from src.api.impl.http_client import RequestsHttpClient
from src.controllers.post_controller import PostController


def build_post_controller() -> PostController:
    client = RequestsHttpClient()
    return PostController(client)
