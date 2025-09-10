from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status

from src.adapters.score import (
    create_in_to_internal,
    create_internal_to_out,
    score_internal_to_out,
)
from src.assembly import build_score_controller
from src.controllers.score import ScoreController
from src.database.config import get_db
from src.models.incoming.create_score import CreateScoreRequest
from src.models.internal.filters import ScoreFilter
from src.models.out.create_score import CreateScoreResponse
from src.models.out.delete_score import DeleteScoreResponse
from src.models.out.get_score_count import GetScoreCountResponse
from src.models.out.reset import ResetResponse
from src.models.out.score import ScoreResponse

router = APIRouter(prefix="/scores")


@router.post(
    "/", response_model=CreateScoreResponse, status_code=status.HTTP_201_CREATED
)
def create_score(
    score_request: CreateScoreRequest,
    controller: ScoreController = Depends(build_score_controller),
    db=Depends(get_db),
) -> CreateScoreResponse:
    new_score = controller.create_score(db, create_in_to_internal(score_request))

    return create_internal_to_out(new_score)


@router.get(
    "/count", response_model=GetScoreCountResponse, status_code=status.HTTP_200_OK
)
def get_score_count(
    controller: ScoreController = Depends(build_score_controller), db=Depends(get_db)
) -> GetScoreCountResponse:
    count = controller.get_count(db)
    return GetScoreCountResponse(count=count)


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping() -> str:
    return "pong"


@router.post("/reset", response_model=ResetResponse, status_code=status.HTTP_200_OK)
def reset(
    controller: ScoreController = Depends(build_score_controller), db=Depends(get_db)
) -> ResetResponse:
    controller.reset(db)

    return ResetResponse(msg="Todos los datos fueron eliminados")


@router.get("/", response_model=list[ScoreResponse], status_code=status.HTTP_200_OK)
def get_scores(
    offers: Optional[str] = Query(
        None,
        description="Comma-separated offer IDs, e.g. ?offers=abc,def,ghi",
    ),
    controller: ScoreController = Depends(build_score_controller),
    db=Depends(get_db),
) -> list[ScoreResponse]:
    # Parse comma-separated offers -> list[str]
    offers_list = offers.split(",") if offers else None
    scores = controller.get_scores(db, ScoreFilter(offers_ids=offers_list))

    return [score_internal_to_out(score) for score in scores]


@router.get("/{id}", response_model=ScoreResponse, status_code=status.HTTP_200_OK)
def get_score(
    id: UUID = Path(description="The ID of the score to retrieve"),
    controller: ScoreController = Depends(build_score_controller),
    db=Depends(get_db),
) -> ScoreResponse:
    score = controller.get_score(db, id)

    return score_internal_to_out(score)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_score(
    id: UUID = Path(description="The ID of the score to delete"),
    controller: ScoreController = Depends(build_score_controller),
    db=Depends(get_db),
) -> DeleteScoreResponse:
    controller.delete_score(db, id)

    return DeleteScoreResponse(msg="la utilidad fue eliminada")
