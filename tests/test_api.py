

TEST_ROOM = {"entities": {
    "a": {"x": 0, "y": 0, "type": "player", "ai": "pathfinder", "score": 0},
    "b": {"x": 1, "y": 1, "type": "block"},
    "c": {"x": 1, "y": 0, "type": "coin"}
}}


TEST_ROOM_2 = {"entities": {
    "d": {"x": 0, "y": 0, "type": "player", "ai": "manual", "score": 0}
}}


def test_step(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM)
    room_before = client.get("/api/rooms/testroom").json()

    response = client.post("/api/rooms/testroom/step")
    assert response.status_code == 200

    room_after = client.get("/api/rooms/testroom").json()
    assert not room_before == room_after


def test_get_step(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM)
    response = client.get("/api/rooms/testroom/step")
    assert response.status_code == 200
    step = response.json()
    assert step == 0

    client.post("/api/rooms/testroom/step")
    step = client.get("/api/rooms/testroom/step").json()
    assert step == 1


def test_score(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM)
    room = client.get("/api/rooms/testroom").json()
    score = [entity["score"]
             for entity in room["entities"].values() if "score" in entity][0]
    assert score == 0

    client.post("/api/rooms/testroom/step")
    room = client.get("/api/rooms/testroom").json()
    score = [entity["score"]
             for entity in room["entities"].values() if "score" in entity][0]
    assert score != 0


def test_manual_ai(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM_2)
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == 0
    assert player["y"] == 0

    client.put(
        "/api/rooms/testroom/entities/d/setmove",
        json="move_up")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == 0
    assert player["y"] == 1

    client.put(
        "/api/rooms/testroom/entities/d/setmove",
        json="move_down")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == 0
    assert player["y"] == 0

    client.put(
        "/api/rooms/testroom/entities/d/setmove",
        json="move_left")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == -1
    assert player["y"] == 0

    client.put(
        "/api/rooms/testroom/entities/d/setmove",
        json="move_right")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == 0
    assert player["y"] == 0

    # Don't continue moving
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == 0
    assert player["y"] == 0
