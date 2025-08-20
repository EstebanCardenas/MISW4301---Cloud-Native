from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.internal.post import Post
from src.models.internal.post_filter import PostFilter
from src.repositories.posts_repository import PostsRepository


class DbPostsRepository(PostsRepository):
    """Database implementation of the PostsRepository interface"""

    def create(self, db: Session, post: Post) -> Post:
        """Create a new post in the database"""
        db.add(post)
        db.commit()
        db.refresh(post)

        return post

    def get_by_id(self, db: Session, id: str) -> Optional[Post]:
        """Get a post by ID from the database"""
        return db.query(Post).filter(Post.id == id).first()

    def get_all(self, db: Session, filters: PostFilter | None = None) -> List[Post]:
        """Get all posts from the database"""
        query = db.query(Post)
        if filters:
            if filters.route:
                query = query.filter(Post.route_id == filters.route)
            if filters.owner:
                query = query.filter(Post.user_id == filters.owner)
        return query.all()

    def get_count(self, db: Session) -> int:
        """Get the count of all posts in the database"""
        return db.query(Post).count()

    def update(self, db: Session, post: Post) -> Post:
        """Update an existing post in the database"""
        db.merge(post)
        db.commit()
        db.refresh(post)

        return post

    def delete(self, db: Session, id: str) -> None:
        """Delete a post by ID from the database"""
        post = db.query(Post).filter(Post.id == id).first()

        if post:
            db.delete(post)
            db.commit()

    def reset(self, db: Session) -> None:
        """Reset the posts table in the database"""
        db.query(Post).delete()
        db.commit()
