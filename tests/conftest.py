from fastapi.testclient import TestClient
import pytest

from app import create_app


@pytest.fixture
def client():
    # Create a new app for each test to avoid complicated cleanup
    app = create_app()
    return TestClient(app)
