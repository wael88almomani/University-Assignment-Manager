from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base
from app.core.dependencies import get_db
from app.main import app

# Ensure SQLAlchemy metadata includes all models.
from app.data.models.assignment_model import Assignment  # noqa: F401
from app.data.models.course_model import Course  # noqa: F401
from app.data.models.enrollment_model import Enrollment  # noqa: F401
from app.data.models.section_model import Section  # noqa: F401
from app.data.models.submission_model import Submission  # noqa: F401
from app.data.models.user_model import User  # noqa: F401

TEST_DATABASE_URL = "sqlite:///./test_uam.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
