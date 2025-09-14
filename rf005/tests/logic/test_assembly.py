from src.api.impl.http_client import RequestsHttpClient
from src.assembly import build_post_controller
from src.controllers.post_controller import PostController


def test_build_post_controller_injects_http_client():
    controller = build_post_controller()
    assert isinstance(controller, PostController)
    assert isinstance(controller.http_client, RequestsHttpClient)
