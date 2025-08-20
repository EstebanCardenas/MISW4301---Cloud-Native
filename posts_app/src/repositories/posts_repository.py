from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.internal.post import Post
from src.models.internal.post_filter import PostFilter


class PostsRepository(ABC):
    """Offer repository interface"""

    @abstractmethod
    def create(self, db: Session, post: Post) -> Post:
        """Create a new post"""
        pass

    @abstractmethod
    def get_by_id(self, db: Session, id: str) -> Optional[Post]:
        """Get a post by ID"""
        pass

    @abstractmethod
    def get_all(self, db: Session, filters: PostFilter | None = None) -> List[Post]:
        """Get all posts"""
        pass

    @abstractmethod
    def get_count(self, db: Session) -> int:
        """Get the count of all posts"""
        pass

    @abstractmethod
    def update(self, db: Session, post: Post) -> Post:
        """Update an existing post"""
        pass

    @abstractmethod
    def delete(self, db: Session, id: str) -> None:
        """Delete a post by ID"""
        pass

    @abstractmethod
    def reset(self, db: Session) -> None:
        """Reset the database"""
        pass
