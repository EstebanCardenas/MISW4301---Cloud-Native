from typing import List

from src.models.internal.offer import Offer, OfferItem
from src.models.internal.post import Post
from src.models.internal.route import Route, RouteItem
from src.models.out.rf005_response import RF005Data, RF005Response


def info_to_response(
    post: Post, route: RouteItem, offers: List[OfferItem] = []
) -> RF005Response:
    return RF005Response(
        data=RF005Data(
            id=post.id,
            expireAt=post.expire_at,
            route=route,
            plannedStartDate="2000-01-01T00:00:00Z",
            plannedEndDate="2000-01-01T00:00:00Z",
            createdAt=post.created_at,
            offers=offers,
        )
    )
