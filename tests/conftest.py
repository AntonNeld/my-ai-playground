from fastapi.testclient import TestClient
import pytest

from app import create_app

app = create_app()
test_client = TestClient(app)


@pytest.fixture
def client():
    test_client.post("/api/state/clear")
    return test_client
