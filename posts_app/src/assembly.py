from src.controllers.post_controller import PostController
from src.repositories.impl.db_posts_repository import DbPostsRepository

repository = DbPostsRepository()


def build_post_controller() -> PostController:
    return PostController(repository)
