import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base
from app.dependencies import get_db
from app.main import app

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """
    Override the production database dependency with the test database.

    Yields:
        An active SQLAlchemy session connected to the test database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """
    Provide a clean database for each test function.

    Creates all tables before the test runs and drops them after,
    ensuring complete test isolation.

    Yields:
        An active SQLAlchemy session connected to the test database.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Provide a FastAPI TestClient configured to use the test database.

    Args:
        db_session: The test database session fixture.

    Returns:
        A TestClient instance for making requests to the API.
    """
    return TestClient(app)
