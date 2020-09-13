import pytest


@pytest.fixture
def template(client):
    client.put("/api/templates/testtemplate", json={
        "entities": [
            {
                "label": "entityOne",
                "ai": {"kind": "singular", "move": "move_left"},
                "pickupper": {"inventory": [{}]},
                "scoring": {"kind": "heldItems"},
                "position": {"x": 0, "y": 0}
            },
            {
                "label": "entityTwo",
                "score": 0
            },
        ]
    })
    return "testtemplate"


def test_evaluate(client, template):
    response = client.post(
        "/api/evaluate", json={"template": template, "duration": 3})
    assert response.status_code == 200
    assert response.json() == {"scores": {"entityOne": 1, "entityTwo": 0}}


def test_profile_time(client, template):
    response = client.post(
        "/api/evaluate", json={"template": template, "duration": 3,
                               "profileTime": True})
    assert response.status_code == 200
    assert "processTime" in response.json()
    assert "aiTimes" in response.json()
    assert "entityOne" in response.json()["aiTimes"]
