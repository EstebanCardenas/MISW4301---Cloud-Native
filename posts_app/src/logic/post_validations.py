from datetime import datetime, timezone

from src.models.internal.post import Post


def validatePost(post: Post) -> str | None:
    """Validates the post data"""
    if not post.route_id:
        return "Route ID is required."
    if not post.user_id:
        return "User ID is required."
    if not post.expire_at:
        return "Expiration date is required."
    else:
        if post.expire_at <= datetime.now(timezone.utc):
            return "La fecha expiración no es válida"
    return None
