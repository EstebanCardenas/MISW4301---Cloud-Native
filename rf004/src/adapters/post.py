from src.models.incoming.posts import GetPostResponse
from src.models.internal.post import Post


def post_in_to_internal(post: GetPostResponse) -> Post:
    return Post(
        id=post.id,
        route_id=post.routeId,
        user_id=post.userId,
        created_at=post.createdAt,
        expire_at=post.expireAt,
    )
