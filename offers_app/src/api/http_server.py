from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status

from src.adapters.offer import (
    create_in_to_internal,
    create_internal_to_out,
    offer_internal_to_out,
)
from src.assembly import build_offer_controller
from src.controllers.offer import OfferController
from src.database.config import get_db
from src.models.incoming.create_offer import CreateOfferRequest
from src.models.internal.filters import OfferFilter
from src.models.out.create_offer import CreateOfferResponse
from src.models.out.delete_offer import DeleteOfferResponse
from src.models.out.get_offer_count import GetOfferCountResponse
from src.models.out.offer import OfferResponse
from src.models.out.reset import ResetResponse

router = APIRouter(prefix="/offers")


@router.post(
    "/", response_model=CreateOfferResponse, status_code=status.HTTP_201_CREATED
)
def create_offer(
    offer: CreateOfferRequest,
    controller: OfferController = Depends(build_offer_controller),
    db=Depends(get_db),
) -> CreateOfferResponse:
    new_offer = controller.create_offer(db, create_in_to_internal(offer))

    return create_internal_to_out(new_offer)


@router.get(
    "/count", response_model=GetOfferCountResponse, status_code=status.HTTP_200_OK
)
def get_offer_count(
    controller: OfferController = Depends(build_offer_controller), db=Depends(get_db)
) -> GetOfferCountResponse:
    count = controller.get_count(db)
    return GetOfferCountResponse(count=count)


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping() -> str:
    return "pong"


@router.post("/reset", response_model=ResetResponse, status_code=status.HTTP_200_OK)
def reset(
    controller: OfferController = Depends(build_offer_controller), db=Depends(get_db)
) -> ResetResponse:
    controller.reset(db)

    return ResetResponse(msg="Todos los datos fueron eliminados")


@router.get("/", response_model=list[OfferResponse], status_code=status.HTTP_200_OK)
def get_offers(
    post: UUID = Query(None, description="Filter offers by post ID"),
    owner: UUID = Query(None, description="Filter offers by user ID"),
    controller: OfferController = Depends(build_offer_controller),
    db=Depends(get_db),
) -> list[OfferResponse]:
    offers = controller.get_offers(db, OfferFilter(post_id=post, user_id=owner))

    return [offer_internal_to_out(offer) for offer in offers]


@router.get("/{id}", response_model=OfferResponse, status_code=status.HTTP_200_OK)
def get_offer(
    id: UUID = Path(description="The ID of the offer to retrieve"),
    controller: OfferController = Depends(build_offer_controller),
    db=Depends(get_db),
) -> OfferResponse:
    offer = controller.get_offer(db, id)

    return offer_internal_to_out(offer)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_offer(
    id: UUID = Path(description="The ID of the offer to delete"),
    controller: OfferController = Depends(build_offer_controller),
    db=Depends(get_db),
) -> DeleteOfferResponse:
    controller.delete_offer(db, id)

    return DeleteOfferResponse(msg="la oferta fue eliminada")
