import pytest

from test_utils import is_uuid

RESOURCE_TYPES = [
    {
        "resource": "rooms",
        "parents": [],
        "example": {
            "entities": {
                "a": {"x": 0, "y": 0, "type": "player",
                      "ai": "pathfinder", "score": 0},
                "b": {"x": 1, "y": 1, "type": "block"},
                "c": {"x": 1, "y": 0, "type": "coin"}
            }
        }
    },
    {
        "resource": "entities",
        "parents": [{"resource": "rooms", "id": "testroom",
                     "body": {"entities": {}}}],
        "example": {
            "x": 0,
            "y": 0,
            "type": "player",
            "ai": "pathfinder",
            "score": 0
        }
    }
]


@pytest.mark.parametrize("resource", RESOURCE_TYPES,
                         ids=[r["resource"] for r in RESOURCE_TYPES])
class TestResource:

    @pytest.fixture
    def base_url(self, client, resource):
        # If needed, set up a parent that can contain the resource
        parent_url = "/api"
        for parent in resource["parents"]:
            parent_url += f'/{parent["resource"]}/{parent["id"]}'
            client.put(parent_url, json=parent["body"])
        return f'{parent_url}/{resource["resource"]}'

    @pytest.fixture(params=["post", "put"])
    def existing_resource(self, client, base_url, resource, request):
        if request.param == "post":
            resource_id = client.post(
                base_url, json=resource["example"]).json()
        elif request.param == "put":
            resource_id = client.put(
                f"{base_url}/someid", json=resource["example"]).json()
        return {"id": resource_id, "resource": resource["example"]}

    def test_post_resource(self, client, base_url, resource):
        response = client.post(base_url, json=resource["example"])
        assert response.status_code == 200
        resource_id = response.json()
        assert is_uuid(resource_id)

    def test_put_resource(self, client, base_url, resource):
        response = client.put(
            f'{base_url}/someid', json=resource["example"])
        assert response.status_code == 200
        assert response.json() == 'someid'

    def test_get_resource(self, client, base_url, resource, existing_resource):
        response = client.get(f'{base_url}/{existing_resource["id"]}')
        assert response.status_code == 200
        assert response.json() == existing_resource["resource"]
