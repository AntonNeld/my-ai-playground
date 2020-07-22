import pytest


@pytest.mark.parametrize("method", ["post", "put"])
def test_create_room_from_template(client, method):
    client.put("/api/templates/testtemplate", json={
        "entities": [{"x": 0, "y": 0, "ai": {"kind": "random"},
                      "looksLike": "player", "canPickup": True},
                     {"x": 1, "y": 0,
                      "pickup": {"kind": "addScore", "score": 1},
                      "looksLike": "coin"}]
    })
    if method == "post":
        response = client.post("/api/rooms?from_template=testtemplate")
    elif method == "put":
        response = client.put(
            "/api/rooms/testroom?from_template=testtemplate")
    assert response.status_code == 200
    room_id = response.json()

    response = client.get(f"/api/rooms/{room_id}")
    assert response.status_code == 200
    room = response.json()
    assert {"x": 0, "y": 0, "ai": {"kind": "random"},
            "looksLike": "player",
            "canPickup": True} in room["entities"].values()
    assert {"x": 1, "y": 0,
            "pickup": {"kind": "addScore", "score": 1},
            "looksLike": "coin"} in room["entities"].values()
    assert room["steps"] == 0


@pytest.mark.parametrize("method", ["post", "put"])
def test_body_required_if_no_template(client, method):
    if method == "post":
        response = client.post("/api/rooms")
    elif method == "put":
        response = client.put(
            "/api/rooms/testroom")
    assert response.status_code == 422


def test_step(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {
            "a": {"x": 0, "y": 0,
                  "ai": {"kind": "pathfinder"}, "score": 0,
                  "looksLike": "player", "canPickup": True},
            "b": {"x": 1, "y": 0, "type": "coin",
                  "pickup": {"kind": "addScore", "score": 1},
                  "looksLike": "coin"}
        }
    })

    response = client.post("/api/rooms/testroom/step")
    assert response.status_code == 200

    room_after = client.get("/api/rooms/testroom").json()
    assert room_after == {
        "steps": 1,
        "entities": {
            "a": {"x": 1, "y": 0,
                  "ai": {"kind": "pathfinder", "plan": []}, "score": 1,
                  "looksLike": "player", "canPickup": True}
        }
    }
