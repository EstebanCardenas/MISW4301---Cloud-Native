from src.models.incoming.create_score import CreateScoreRequest, OfferSize
from src.models.internal.score import Score
from src.models.out.create_score import CreateScoreResponse
from src.models.out.score import ScoreResponse


def create_in_to_internal(score: CreateScoreRequest) -> Score:
    
    ocupation_percentage = 0
    if (score.bagSize == OfferSize.SMALL):
        ocupation_percentage = 0.25
    elif (score.bagSize == OfferSize.MEDIUM):
        ocupation_percentage = 0.5
    elif (score.bagSize == OfferSize.LARGE):
        ocupation_percentage = 1

    score_value = score.offerAmount - (score.bagCost * ocupation_percentage)

    return Score(
        offerId=score.offerId,
        value=score_value,
    )


def create_internal_to_out(score: Score) -> CreateScoreResponse:
    return CreateScoreResponse(id=score.id, createdAt=score.createdAt)


def score_internal_to_out(score: Score) -> ScoreResponse:
    return ScoreResponse(
        id=str(score.id),
        offerId=score.offerId,
        value=score.value,
        createdAt=score.createdAt,
    )
