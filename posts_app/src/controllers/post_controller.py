from typing import List

from sqlalchemy.orm import Session

from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.logic.post_validations import validatePost
from src.models.internal.post import Post
from src.models.internal.post_filter import PostFilter
from src.repositories.posts_repository import PostsRepository


class PostController:
    def __init__(self, posts_repository: PostsRepository):
        self.posts_repository = posts_repository

    def create_post(self, db: Session, post: Post) -> Post:
        result = validatePost(post)

        if result is not None:
            raise ApiException(type=ApiExceptionType.VALIDATION_FAILED, detail=result)

        return self.posts_repository.create(db, post)

    def get_count(self, db: Session) -> int:
        return self.posts_repository.get_count(db)

    def get_posts(self, db: Session, filters: PostFilter | None = None) -> List[Post]:
        return self.posts_repository.get_all(db, filters)

    def get_post(self, db: Session, id: str) -> Post:
        post = self.posts_repository.get_by_id(db, id)

        if not post:
            raise ApiException(type=ApiExceptionType.NOT_FOUND, detail="Post not found")

        return post

    def delete_post(self, db: Session, id: str) -> None:
        post = self.posts_repository.get_by_id(db, id)

        if not post:
            raise ApiException(type=ApiExceptionType.NOT_FOUND, detail="Post not found")

        self.posts_repository.delete(db, id)

    def reset(self, db: Session) -> None:
        self.posts_repository.reset(db)
