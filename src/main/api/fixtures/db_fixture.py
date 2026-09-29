import pytest
from src.main.api.db.engine import SessionLocal, engine


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()