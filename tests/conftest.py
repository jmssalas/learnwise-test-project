import os

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["LLM_SERVICE"] = "mock"
os.environ["SMS_PROVIDER"] = "mock"

from app.db.models import Base
from app.db.sqlite import SQLite
from app.main import app
from app.services.storage.storage_service import StorageService


@pytest.fixture
def database() -> SQLite:
    database = SQLite("sqlite:///:memory:")
    Base.metadata.create_all(database.engine)
    yield database
    database.close()


@pytest.fixture
def storage(database: SQLite) -> StorageService:
    return StorageService(database)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)