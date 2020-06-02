

TEST_ROOM = {
    "steps": 0,
    "entities": {
        "a": {"x": 0, "y": 0, "type": "player",
              "ai": "pathfinder", "score": 0},
        "b": {"x": 1, "y": 0, "type": "coin"}
    }
}


def test_step(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {
            "a": {"x": 0, "y": 0, "type": "player",
                  "ai": "pathfinder", "score": 0},
            "b": {"x": 1, "y": 0, "type": "coin"}
        }
    })

    response = client.post("/api/rooms/testroom/step")
    assert response.status_code == 200

    room_after = client.get("/api/rooms/testroom").json()
    assert room_after == {
        "steps": 1,
        "entities": {
            "a": {"x": 1, "y": 0, "type": "player",
                  "ai": "pathfinder", "score": 1}
        }
    }


def test_manual_ai(client):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {
            "a": {"x": 0, "y": 0, "type": "player", "ai": "manual", "score": 0}
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
