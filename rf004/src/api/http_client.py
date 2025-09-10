from abc import ABC, abstractmethod

from pydantic import UUID4

from models.internal.offer import BaseOffer, Offer
from src.models.internal.post import Post
from src.models.internal.user import User


class HttpClient(ABC):
    @abstractmethod
    def get_post(self, post_id: UUID4) -> Post:
        pass

    @abstractmethod
    def create_offer(self, data: BaseOffer) -> Offer:
        pass

    @abstractmethod
    def get_user_info(self, auth_token: UUID4) -> User:
        pass
