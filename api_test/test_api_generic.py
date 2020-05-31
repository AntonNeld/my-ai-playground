import pytest
from fastapi.testclient import TestClient

from test_utils import is_uuid
from main import create_app

RESOURCE_TYPES = [
    {
        "resource": "rooms",
        "parents": [],
        "example": []
    },
    {
        "resource": "entities",
        "parents": [{"resource": "rooms", "id": "testroom", "body": []}],
        "example": {"x": 0, "y": 0, "type": "player", "ai": "pathfinder"}
    }
]


@pytest.fixture
def client():
    # Create a new app for each test to avoid complicated cleanup
    app = create_app()
    return TestClient(app)


@pytest.mark.parametrize("resource", RESOURCE_TYPES)
class TestResource:

    @pytest.fixture
    def base_url(self, client, resource):
        # If needed, set up a parent that can contain the resource
        parent_url = "/api"
        for parent in resource["parents"]:
            parent_url += f'/{parent["resource"]}/{parent["id"]}'
            client.put(parent_url, json=parent["body"])
        return f'{parent_url}/{resource["resource"]}'

    def test_post_resource(self, client, base_url, resource):
        response = client.post(base_url, json=resource["example"])
        assert response.status_code == 200
        resource_id = response.json()
        assert is_uuid(resource_id)

    def test_put_resource(self, client, base_url, resource):
        response = client.put(
            f'{base_url}/someid', json=resource["example"])
        assert response.status_code == 200
