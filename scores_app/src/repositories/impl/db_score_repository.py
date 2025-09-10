from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.internal.filters import ScoreFilter
from src.models.internal.score import Score
from src.repositories.score_repository import ScoreRepository


class DbScoreRepository(ScoreRepository):
    """Database implementation of the ScoreRepository interface"""

    def create(self, db: Session, score: Score) -> Score:
        """Create a new score in the database"""
        db.add(score)
        db.commit()
        db.refresh(score)

        return score

    def get_by_id(self, db: Session, id: str) -> Optional[Score]:
        """Get a score by ID from the database"""
        return db.query(Score).filter(Score.id == id).first()

    def get_all(self, db: Session, filters: ScoreFilter | None = None) -> List[Score]:
        """Get all scores from the database"""
        query = db.query(Score)

        if filters:
            if filters.offers_ids:
                query = query.filter(Score.offer_id.in_(filters.offers_ids))

        return query.all()

    def get_count(self, db: Session) -> int:
        """Get the count of all scores in the database"""
        return db.query(Score).count()

    def delete(self, db: Session, id: str) -> None:
        """Delete a score by ID from the database"""
        score = db.query(Score).filter(Score.id == id).first()

        if score:
            db.delete(score)
            db.commit()

    def reset(self, db: Session) -> None:
        """Reset the scores table in the database"""
        db.query(Score).delete()
        db.commit()
