from datetime import datetime
from uuid import UUID

from src.api.http_client import HttpClient
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.internal.offer import BaseOffer, Offer


class OfferController:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def create_offer(self, user_id: UUID, post_id: UUID, offer: BaseOffer) -> Offer:
        print("Getting post")
        self.http_client.offers_service_health_check()
        post = self.http_client.get_post(post_id)
        print(post)

        if post.user_id == user_id:
            raise ApiException(
                ApiExceptionType.VALIDATION_FAILED,
                "La publicación pertenece al mismo usuario que crea la oferta",
            )

        if post.expire_at < datetime.now():
            raise ApiException(
                ApiExceptionType.VALIDATION_FAILED,
                "La publicación seleccionada ya expiró",
            )

        print("Getting route")
        route = self.http_client.get_route_info(post.route_id)
        print("Creating offer")
        new_offer = self.http_client.create_offer(offer)

        try:
            print("Creating score")
            self.http_client.create_score(
                new_offer.offer, new_offer.size, route.bag_cost, new_offer.id
            )
        except ApiException as e:
            print("Deleting offer due to score creation failure")
            print(e)
            self.http_client.delete_offer(new_offer.id)
            raise e

        return new_offer
