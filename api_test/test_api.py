from test_utils import is_uuid


TEST_ROOM = [
    {"x": 0, "y": 0, "type": "player", "ai": "pathfinder"},
    {"x": 1, "y": 1, "type": "block"},
    {"x": 1, "y": 0, "type": "coin"}
]


TEST_ROOM_2 = [
    {"x": 0, "y": 0, "type": "player", "ai": "manual"}
]


def same(first, second, strip_generated=True):
    """
    Tests if two rooms/views are equal.
    Order doesn't matter, and generated attributes are optionally removed.
    """
    if len(first) != len(second):
        return False
    if strip_generated:
        generated_attributes = ["id", "score"]
        first = [{key: entity[key] for key in entity if
                  key not in generated_attributes} for entity in first]
        second = [{key: entity[key] for key in entity if
                   key not in generated_attributes} for entity in second]
    for entity in first:
        if entity not in second:
            return False
    return True


def test_helper_same():
    assert same(TEST_ROOM, TEST_ROOM)
    assert not same(TEST_ROOM, TEST_ROOM_2)


def test_create_room(client):
    response = client.post("/api/rooms", json=TEST_ROOM)
    assert response.status_code == 200
    room_id = response.json()
    assert is_uuid(room_id)

    response = client.get("/api/rooms")
    assert room_id in response.json()

    response = client.get(f"/api/rooms/{room_id}")
    assert same(response.json(), TEST_ROOM)
    assert "id" in response.json()[0]


def test_create_two_rooms(client):
    room_id_1 = client.post("/api/rooms", json=TEST_ROOM).json()
    room_id_2 = client.post("/api/rooms", json=TEST_ROOM_2).json()

    response = client.get("/api/rooms")
    assert room_id_1 in response.json()
    assert room_id_2 in response.json()

    room_1 = client.get(f"/api/rooms/{room_id_1}").json()
    room_2 = client.get(f"/api/rooms/{room_id_2}").json()
    assert same(room_1, TEST_ROOM)
    assert same(room_2, TEST_ROOM_2)


def test_replace_room(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM)
    room_1 = client.get("/api/rooms/testroom").json()
    assert same(room_1, TEST_ROOM)

    client.put("/api/rooms/testroom", json=TEST_ROOM_2)
    room_2 = client.get("/api/rooms/testroom").json()
    assert same(room_2, TEST_ROOM_2)


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
    assert not same(room_before, room_after)


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
    score = [entity["score"] for entity in room if "score" in entity][0]
    assert score == 0

    client.post("/api/rooms/testroom/step")
    room = client.get("/api/rooms/testroom").json()
    score = [entity["score"] for entity in room if "score" in entity][0]
    assert score != 0


def test_list_get_entity(client):
    client.put("/api/rooms/testroom", json=TEST_ROOM)

    response = client.get("/api/rooms/testroom/entities")
    assert response.status_code == 200
    entity_id = response.json()[0]
    assert is_uuid(entity_id)

    response = client.get(
        f"/api/rooms/testroom/entities/{entity_id}")
    assert response.status_code == 200
    entity = response.json()
    assert {key: entity[key]
            for key in entity if key not in ["id", "score"]} in TEST_ROOM


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
    player = client.get("/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0
    player_id = player["id"]

    client.put(
        f"/api/rooms/testroom/agents/{player_id}/setmove",
        json="move_up")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 1

    client.put(
        f"/api/rooms/testroom/agents/{player_id}/setmove",
        json="move_down")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0

    client.put(
        f"/api/rooms/testroom/agents/{player_id}/setmove",
        json="move_left")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom").json()[0]
    assert player["x"] == -1
    assert player["y"] == 0

    client.put(
        f"/api/rooms/testroom/agents/{player_id}/setmove",
        json="move_right")
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0

    # Don't continue moving
    client.post("/api/rooms/testroom/step")
    player = client.get("/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0
