import os

# 🔹 Establece DATABASE_URL antes de cualquier import de la app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest

from src.database.config import Base
from tests.unit.test_main import test_engine  # Import your test engine


@pytest.fixture(autouse=True)
def reset_db():
    """Drop and recreate all tables before each test."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
