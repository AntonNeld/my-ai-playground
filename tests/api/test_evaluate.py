import pytest


@pytest.fixture
def challenge(client):
    client.put("/api/challenges/testchallenge", json={
        "template": {
            "templateType": "raw",
            "entities": [
                {
                    "label": "entityOne",
                    "pickupper": {"inventory": [{}]},
                    "scoring": {"kind": "heldItems"},
                    "position": {"x": 0, "y": 0}
                },
                {
                    "label": "entityTwo",
                    "score": 0
                },
                {"score": 5}
            ]
        }
    })
    return "testchallenge"


@pytest.fixture
def challenge_with_variants(client):
    client.put("/api/challenges/testchallenge", json={
        "variants": {
            "variantOne": {
                "entities[0].scoring": {"kind": "heldItems"},
                "entities[0].score": 0
            },
            "variantTwo": {}
        },
        "template": {
            "templateType": "raw",
            "entities": [
                {
                    "label": "entityOne",
                    "pickupper": {"inventory": [{}]},
                    "score": 2,
                    "position": {"x": 0, "y": 0}
                },
                {
                    "label": "entityTwo",
                    "score": 0
                },
                {"score": 5}
            ]
        }
    })
    return "testchallenge"


def test_evaluate(client, challenge):
    response = client.post(
        "/api/evaluate", json={"challenge": challenge, "duration": 3})
    assert response.status_code == 200
    assert response.json() == {
        "entities": {
            "entityOne": {"score": 1},
            "entityTwo": {"score": 0}
        }
    }


def test_profile_time(client, challenge):
    response = client.post(
        "/api/evaluate", json={"challenge": challenge, "duration": 3,
                               "profileTime": True})
    assert response.status_code == 200
    assert "processTime" in response.json()
    assert "time" in response.json()["entities"]["entityOne"]
    assert "time" in response.json()["entities"]["entityTwo"]


def test_profile_memory(client, challenge):
    response = client.post(
        "/api/evaluate", json={"challenge": challenge, "duration": 3,
                               "profileMemory": True})
    assert response.status_code == 200
    assert "memory" in response.json()["entities"]["entityOne"]
    assert "memory" in response.json()["entities"]["entityTwo"]


def test_evaluate_variants(client, challenge_with_variants):
    response = client.post(
        "/api/evaluate", json={"challenge": challenge_with_variants,
                               "duration": 3})
    assert response.status_code == 200
    assert response.json() == {
        "entities": {
            "variantOne:entityOne": {"score": 1},
            "variantOne:entityTwo": {"score": 0},
            "variantTwo:entityOne": {"score": 2},
            "variantTwo:entityTwo": {"score": 0}
        }
    }


def test_profile_time_variants(client, challenge_with_variants):
    response = client.post(
        "/api/evaluate", json={"challenge": challenge_with_variants,
                               "duration": 3,
                               "profileTime": True})
    assert response.status_code == 200
    assert "processTime" in response.json()
    for label in ["variantOne:entityOne", "variantOne:entityTwo",
                  "variantTwo:entityOne", "variantTwo:entityTwo"]:
        assert "time" in response.json()["entities"][label]


def test_profile_memory_variants(client, challenge_with_variants):
    response = client.post(
        "/api/evaluate", json={"challenge": challenge_with_variants,
                               "duration": 3,
                               "profileMemory": True})
    assert response.status_code == 200
    for label in ["variantOne:entityOne", "variantOne:entityTwo",
                  "variantTwo:entityOne", "variantTwo:entityTwo"]:
        assert "memory" in response.json()["entities"][label]
