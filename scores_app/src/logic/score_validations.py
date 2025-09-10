from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.models.internal.score import Score


def validateScore(db: Session, score: Score) -> str | None:
    # 1. Validar que el offerId no exista ya
    existing_score = (
        db.query(Score).filter(Score.offerId == str(score.offerId)).first()
    )
    if existing_score:
        return "El offerId ya existe"

    return None
