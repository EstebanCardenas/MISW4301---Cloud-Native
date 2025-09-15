from abc import ABC, abstractmethod
from typing import List

from pydantic import UUID4

from src.models.internal.offer import Offer
from src.models.internal.post import Post
from src.models.internal.route import Route, RouteItem
from src.models.internal.score import Score
from src.models.internal.user import User


class HttpClient(ABC):
    @abstractmethod
    def get_post(self, post_id: UUID4, auth_token: str) -> Post:
        pass

    @abstractmethod
    def get_offers(self, post_id: UUID4, auth_token: str) -> List[Offer]:
        pass

    @abstractmethod
    def get_route(self, route_id: UUID4, auth_token: str) -> RouteItem:
        pass

    @abstractmethod
    def get_score(self, offer_id: UUID4, auth_token: str) -> Score:
        pass

    @abstractmethod
    def get_user_info(self, auth_token: str) -> User:
        pass

    @abstractmethod
    def check_urls(self):
        pass
