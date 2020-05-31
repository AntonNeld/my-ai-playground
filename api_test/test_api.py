

TEST_ROOM = {"entities": {
    "a": {"x": 0, "y": 0, "type": "player", "ai": "pathfinder", "score": 0},
    "b": {"x": 1, "y": 1, "type": "block"},
    "c": {"x": 1, "y": 0, "type": "coin"}
}}


TEST_ROOM_2 = {"entities": {
    "d": {"x": 0, "y": 0, "type": "player", "ai": "manual", "score": 0}
}}


def test_create_two_rooms(client):
    room_id_1 = client.post("/api/rooms", json=TEST_ROOM).json()
    room_id_2 = client.post("/api/rooms", json=TEST_ROOM_2).json()

    response = client.get("/api/rooms")
    assert room_id_1 in response.json()
    assert room_id_2 in response.json()

    room_1 = client.get(f"/api/rooms/{room_id_1}").json()
    room_2 = client.get(f"/api/rooms/{room_id_2}").json()
    assert room_1 == TEST_ROOM
    assert room_2 == TEST_ROOM_2


def test_replace_room(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM)
    room_1 = client.get("/api/rooms/testroom").json()
    assert room_1 == TEST_ROOM

    client.put("/api/rooms/testroom", json=TEST_ROOM_2)
    room_2 = client.get("/api/rooms/testroom").json()
    assert room_2 == TEST_ROOM_2


def test_delete_room(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM)
    response = client.delete("/api/rooms/testroom")
    assert response.status_code == 200
    response = client.get("/api/rooms/testroom")
    assert response.status_code == 404


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


def test_list_get_entity(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM)

    response = client.get("/api/rooms/testroom/entities")
    assert response.status_code == 200
    entity_id = response.json()[0]

    response = client.get(
        f"/api/rooms/testroom/entities/{entity_id}")
    assert response.status_code == 200
    entity = response.json()
    assert entity in TEST_ROOM["entities"].values()


def test_update_entity(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM)
    entity_id = client.get(
        "/api/rooms/testroom/entities").json()[0]
    # Take a step to increase the score
    client.post("/api/rooms/testroom/step")

    entity = client.get(
        f"/api/rooms/testroom/entities/{entity_id}").json()
    entity["ai"] = "manual"
    response = client.put(
        f"/api/rooms/testroom/entities/{entity_id}", json=entity)
    assert response.status_code == 200
    response = client.get(
        f"/api/rooms/testroom/entities/{entity_id}")
    assert response.status_code == 200
    new_entity = response.json()
    assert new_entity == entity


def test_manual_ai(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM_2)
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == 0
    assert player["y"] == 0

    client.put(
        "/api/rooms/testroom/agents/d/setmove",
        json="move_up")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == 0
    assert player["y"] == 1

    client.put(
        "/api/rooms/testroom/agents/d/setmove",
        json="move_down")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == 0
    assert player["y"] == 0

    client.put(
        "/api/rooms/testroom/agents/d/setmove",
        json="move_left")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom/entities/d").json()
    assert player["x"] == -1
    assert player["y"] == 0

    client.put(
        "/api/rooms/testroom/agents/d/setmove",
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
