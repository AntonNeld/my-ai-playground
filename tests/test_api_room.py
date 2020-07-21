import pytest


@pytest.mark.parametrize("method", ["post", "put"])
def test_create_room_from_template(client, method):
    client.put("/api/templates/testtemplate", json={
        "entities": [{"x": 0, "y": 0, "ai": {"kind": "manual"},
                      "looksLike": "player"},
                     {"x": 1, "y": 0,
                      "collisionBehavior": "vanish", "scoreOnDestroy": 1,
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
    assert {"x": 0, "y": 0, "ai": {"kind": "manual"},
            "looksLike": "player"} in room["entities"].values()
    assert {"x": 1, "y": 0,
            "collisionBehavior": "vanish",
            "looksLike": "coin",
            "scoreOnDestroy": 1} in room["entities"].values()
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
                  "looksLike": "player"},
            "b": {"x": 1, "y": 0, "type": "coin", "scoreOnDestroy": 1,
                  "collisionBehavior": "vanish", "looksLike": "coin"}
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
                  "looksLike": "player"}
        }
    }


def test_manual_ai(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {
            "a": {"x": 0, "y": 0, "ai": {"kind": "manual"}, "score": 0,
                  "looksLike": "player"}
        }
    })
    player = client.get("/api/rooms/testroom/entities/a").json()
    assert player["x"] == 0
    assert player["y"] == 0

    client.put(
        "/api/rooms/testroom/entities/a/setmove",
        json="move_up")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/a").json()
    assert player["x"] == 0
    assert player["y"] == 1

    client.put(
        "/api/rooms/testroom/entities/a/setmove",
        json="move_down")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/a").json()
    assert player["x"] == 0
    assert player["y"] == 0

    client.put(
        "/api/rooms/testroom/entities/a/setmove",
        json="move_left")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/a").json()
    assert player["x"] == -1
    assert player["y"] == 0

    client.put(
        "/api/rooms/testroom/entities/a/setmove",
        json="move_right")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/a").json()
    assert player["x"] == 0
    assert player["y"] == 0

    # Don't continue moving
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/a").json()
    assert player["x"] == 0
    assert player["y"] == 0
