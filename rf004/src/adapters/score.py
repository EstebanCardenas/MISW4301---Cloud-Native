from src.models.incoming.score import CreateScoreResponse
from src.models.internal.score import Score


def create_score_in_to_internal(data: CreateScoreResponse) -> Score:
    return Score(
        id=data.id,
        created_at=data.createdAt,
    )
