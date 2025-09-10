from src.controllers.score import ScoreController
from src.repositories.impl.db_score_repository import DbScoreRepository

repository = DbScoreRepository()


def build_score_controller() -> ScoreController:
    return ScoreController(repository)
