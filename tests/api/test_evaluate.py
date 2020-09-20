import pytest


@pytest.fixture
def challenge(client):
    client.put("/api/challenges/testchallenge", json={
        "template": {
            "templateType": "raw",
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
        }
    })
    return "testchallenge"


def test_evaluate(client, challenge):
    response = client.post(
        "/api/evaluate", json={"challenge": challenge, "duration": 3})
    assert response.status_code == 200
    assert response.json() == {"scores": {"entityOne": 1, "entityTwo": 0}}


def test_profile_time(client, challenge):
    response = client.post(
        "/api/evaluate", json={"challenge": challenge, "duration": 3,
                               "profileTime": True})
    assert response.status_code == 200
    assert "processTime" in response.json()
    assert "aiTimes" in response.json()
    assert "entityOne" in response.json()["aiTimes"]


def test_profile_memory(client, challenge):
    response = client.post(
        "/api/evaluate", json={"challenge": challenge, "duration": 3,
                               "profileMemory": True})
    assert response.status_code == 200
    assert "aiMemory" in response.json()
    assert "entityOne" in response.json()["aiMemory"]
