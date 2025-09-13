import uuid
from datetime import datetime, timedelta

from src.adapters.route import get_route_in_to_internal
from src.adapters.score import create_score_in_to_internal
from src.models.incoming.route import RouteInfoResponse
from src.models.incoming.score import CreateScoreResponse
from src.models.internal.route import Route
from src.models.internal.score import Score


def test_types_create_score_in_to_internal() -> None:
    input_data = CreateScoreResponse(
        id=uuid.uuid4(),
        createdAt=datetime.now(),
    )

    internal_score = create_score_in_to_internal(input_data)
    assert isinstance(internal_score.id, uuid.UUID)
    assert isinstance(internal_score.created_at, datetime)


def test_values_create_score_in_to_internal():
    input_data = CreateScoreResponse(
        id=uuid.uuid4(),
        createdAt=datetime.now(),
    )

    internal_score = create_score_in_to_internal(input_data)
    assert internal_score.id == input_data.id
    assert internal_score.created_at == input_data.createdAt
