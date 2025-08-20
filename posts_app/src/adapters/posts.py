from src.models.incoming.create_post_request import CreatePostRequest
from src.models.internal.post import Post
from src.models.out.create_post_response import CreatePostResponse
from src.models.out.post_response import PostResponse


def create_in_to_internal(post: CreatePostRequest) -> Post:
    return Post(
        route_id=post.routeId,
        user_id=post.userId,
        expire_at=post.expireAt,
    )


def create_internal_to_out(post: Post) -> CreatePostResponse:
    return CreatePostResponse(
        id=post.id,
        userId=post.user_id,
        createdAt=post.created_at,
    )


def post_internal_to_out(post: Post) -> PostResponse:
    return PostResponse(
        id=post.id,
        routeId=post.route_id,
        userId=post.user_id,
        createdAt=post.created_at,
        expireAt=post.expire_at,
    )
