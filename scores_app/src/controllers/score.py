from typing import List

from sqlalchemy.orm import Session

from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.logic.score_validations import validateScore
from src.models.internal.filters import ScoreFilter
from src.models.internal.score import Score
from src.repositories.score_repository import ScoreRepository


class ScoreController:

    def __init__(self, score_repository: ScoreRepository):
        self.score_repository = score_repository

    def create_score(self, db: Session, score: Score) -> Score:
        result = validateScore(db, score)

        if result is not None:
            raise ApiException(type=ApiExceptionType.VALIDATION_FAILED, detail=result)

        return self.score_repository.create(db, score)

    def get_count(self, db: Session) -> int:
        return self.score_repository.get_count(db)

    def get_scores(
        self, db: Session, filters: ScoreFilter | None = None
    ) -> List[Score]:
        return self.score_repository.get_all(db, filters)

    def get_score(self, db: Session, id: str) -> Score:
        score = self.score_repository.get_by_id(db, id)

        if not score:
            raise ApiException(
                type=ApiExceptionType.NOT_FOUND, detail="Score not found"
            )

        return score

    def delete_score(self, db: Session, id: str) -> None:
        score = self.score_repository.get_by_id(db, id)

        if not score:
            raise ApiException(
                type=ApiExceptionType.NOT_FOUND, detail="Score not found"
            )

        self.score_repository.delete(db, id)

    def reset(self, db: Session) -> None:
        self.score_repository.reset(db)
