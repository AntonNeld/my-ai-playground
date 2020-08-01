

def test_get_score(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {"a": {
            "pickupper": {"inventory": [{}]},
            "scoring": {"kind": "heldItems"}
        }
        }
    })

    response = client.get(
        "/api/rooms/testroom/entities/a/score")
    assert response.status_code == 200
    assert response.json() == 1


def test_null_score_if_no_scoring(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {"a": {}}
    })

    response = client.get(
        "/api/rooms/testroom/entities/a/score")
    assert response.status_code == 200
    assert response.json() is None
