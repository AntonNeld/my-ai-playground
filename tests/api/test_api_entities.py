

def test_get_evaluated_score(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {
            "a": {
                "label": "me",
                "countTagsScore": {
                    "scoreType": "constant",
                    "addTo": "me",
                    "score": 1,
                    "tags": {"tagOne": 1}
                },
                "position": {"x": 0, "y": 0},
                "tags": ["tagOne"]
            }
        }
    })

    response = client.get(
        "/api/rooms/testroom/entities/a/score")
    assert response.status_code == 200
    assert response.json() == 1


def test_get_accumulated_score(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {
            "a": {
                "score": 5
            }
        }
    })

    response = client.get(
        "/api/rooms/testroom/entities/a/score")
    assert response.status_code == 200
    assert response.json() == 5


def test_get_both_score(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {
            "a": {
                "label": "me",
                "countTagsScore": {
                    "scoreType": "constant",
                    "addTo": "me",
                    "score": 1,
                    "tags": {"tagOne": 1}
                },
                "position": {"x": 0, "y": 0},
                "tags": ["tagOne"],
                "score": 5
            }
        }
    })

    response = client.get(
        "/api/rooms/testroom/entities/a/score")
    assert response.status_code == 200
    assert response.json() == 6


def test_no_score(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {"a": {}}
    })

    response = client.get(
        "/api/rooms/testroom/entities/a/score")
    assert response.status_code == 200
    assert response.json() is None
