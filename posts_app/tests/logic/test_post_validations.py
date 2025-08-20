import uuid
from datetime import datetime, timedelta, timezone

from src.logic.post_validations import validatePost
from src.models.internal.post import Post


def test_invalid_post():
    post = Post(
        id=uuid.uuid4(),
        route_id=None,  # Missing route ID
        user_id=uuid.uuid4(),
        created_at=datetime.now(),
        expire_at=datetime.now() - timedelta(days=1),
    )
    assert validatePost(post) == "Route ID is required."


def test_valid_post():
    post = Post(
        id=uuid.uuid4(),
        route_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        created_at=datetime.now(),
        expire_at=datetime.now(timezone.utc) + timedelta(days=2),
    )
    assert validatePost(post) is None
