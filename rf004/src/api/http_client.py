from abc import ABC, abstractmethod

from pydantic import UUID4

from src.models.internal.offer import BaseOffer, Offer, OfferSize
from src.models.internal.post import Post
from src.models.internal.route import Route
from src.models.internal.score import Score
from src.models.internal.user import User


class HttpClient(ABC):
    @abstractmethod
    def get_post(self, post_id: UUID4) -> Post:
        pass

    @abstractmethod
    def create_offer(self, data: BaseOffer) -> Offer:
        pass

    @abstractmethod
    def get_user_info(self, auth_token: str) -> User:
        pass

    @abstractmethod
    def create_score(
        self, offer_amount: float, offer_size: OfferSize, bag_cost: int, offer_id: UUID4
    ) -> Score:
        pass

    @abstractmethod
    def get_route_info(self, route_id: UUID4) -> Route:
        pass

    @abstractmethod
    def delete_offer(self, offer_id: UUID4) -> None:
        pass

    @abstractmethod
    def offers_service_health_check(self) -> bool:
        pass
