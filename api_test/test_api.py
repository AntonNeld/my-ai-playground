from uuid import UUID

import requests

API_URL = "http://localhost:8300"

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


def valid_id(string):
    try:
        UUID(hex=string)
        return True
    except ValueError:
        return False


def test_helper_same():
    assert same(TEST_ROOM, TEST_ROOM)
    assert not same(TEST_ROOM, TEST_ROOM_2)


def test_helper_valid_id():
    assert valid_id("9f4118fe668843a3a1c847552a69b1db")
    assert not valid_id("banana")


def test_create_room():
    response = requests.post(f"{API_URL}/api/rooms/", json=TEST_ROOM)
    assert response.status_code == 200
    room_id = response.json()
    assert valid_id(room_id)

    response = requests.get(f"{API_URL}/api/rooms/")
    assert room_id in response.json()

    response = requests.get(f"{API_URL}/api/rooms/{room_id}")
    assert same(response.json(), TEST_ROOM)
    assert "id" in response.json()[0]


def test_create_two_rooms():
    room_id_1 = requests.post(f"{API_URL}/api/rooms/", json=TEST_ROOM).json()
    room_id_2 = requests.post(f"{API_URL}/api/rooms/", json=TEST_ROOM_2).json()

    response = requests.get(f"{API_URL}/api/rooms/")
    assert room_id_1 in response.json()
    assert room_id_2 in response.json()

    room_1 = requests.get(f"{API_URL}/api/rooms/{room_id_1}").json()
    room_2 = requests.get(f"{API_URL}/api/rooms/{room_id_2}").json()
    assert same(room_1, TEST_ROOM)
    assert same(room_2, TEST_ROOM_2)


def test_replace_room():
    requests.put(f"{API_URL}/api/rooms/testroom", json=TEST_ROOM)
    room_1 = requests.get(f"{API_URL}/api/rooms/testroom").json()
    assert same(room_1, TEST_ROOM)

    requests.put(f"{API_URL}/api/rooms/testroom", json=TEST_ROOM_2)
    room_2 = requests.get(f"{API_URL}/api/rooms/testroom").json()
    assert same(room_2, TEST_ROOM_2)


def test_delete_room():
    requests.put(f"{API_URL}/api/rooms/testroom", json=TEST_ROOM)
    response = requests.delete(f"{API_URL}/api/rooms/testroom")
    assert response.status_code == 200
    response = requests.get(f"{API_URL}/api/rooms/testroom")
    assert response.status_code == 500  # TODO: Fix to 404


def test_step():
    requests.put(f"{API_URL}/api/rooms/testroom", json=TEST_ROOM)
    room_before = requests.get(f"{API_URL}/api/rooms/testroom").json()

    response = requests.post(f"{API_URL}/api/rooms/testroom/step")
    assert response.status_code == 200

    room_after = requests.get(f"{API_URL}/api/rooms/testroom").json()
    assert not same(room_before, room_after)


def test_get_step():
    requests.put(f"{API_URL}/api/rooms/testroom", json=TEST_ROOM)
    response = requests.get(f"{API_URL}/api/rooms/testroom/step")
    assert response.status_code == 200
    step = response.json()
    assert step == 0

    requests.post(f"{API_URL}/api/rooms/testroom/step")
    step = requests.get(f"{API_URL}/api/rooms/testroom/step").json()
    assert step == 1


def test_score():
    requests.put(f"{API_URL}/api/rooms/testroom", json=TEST_ROOM)
    room = requests.get(f"{API_URL}/api/rooms/testroom").json()
    score = [entity["score"] for entity in room if "score" in entity][0]
    assert score == 0

    requests.post(f"{API_URL}/api/rooms/testroom/step")
    room = requests.get(f"{API_URL}/api/rooms/testroom").json()
    score = [entity["score"] for entity in room if "score" in entity][0]
    assert score != 0


def test_list_get_entity():
    requests.put(f"{API_URL}/api/rooms/testroom", json=TEST_ROOM)

    response = requests.get(f"{API_URL}/api/rooms/testroom/entities")
    assert response.status_code == 200
    entity_id = response.json()[0]
    assert valid_id(entity_id)

    response = requests.get(
        f"{API_URL}/api/rooms/testroom/entities/{entity_id}")
    assert response.status_code == 200
    entity = response.json()
    assert {key: entity[key]
            for key in entity if key not in ["id", "score"]} in TEST_ROOM


def test_update_entity():
    requests.put(f"{API_URL}/api/rooms/testroom", json=TEST_ROOM)
    entity_id = requests.get(
        f"{API_URL}/api/rooms/testroom/entities").json()[0]
    # Take a step to increase the score
    requests.post(f"{API_URL}/api/rooms/testroom/step")

    entity = requests.get(
        f"{API_URL}/api/rooms/testroom/entities/{entity_id}").json()
    entity["ai"] = "manual"
    response = requests.put(
        f"{API_URL}/api/rooms/testroom/entities/{entity_id}", json=entity)
    assert response.status_code == 200
    response = requests.get(
        f"{API_URL}/api/rooms/testroom/entities/{entity_id}")
    assert response.status_code == 200
    new_entity = response.json()
    assert new_entity == entity


def test_manual_ai():
    requests.put(f"{API_URL}/api/rooms/testroom", json=TEST_ROOM_2)
    player = requests.get(f"{API_URL}/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0
    player_id = player["id"]

    requests.put(
        f"{API_URL}/api/rooms/testroom/agents/{player_id}/setmove",
        json="move_up")
    requests.post(f"{API_URL}/api/rooms/testroom/step")
    player = requests.get(f"{API_URL}/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 1

    requests.put(
        f"{API_URL}/api/rooms/testroom/agents/{player_id}/setmove",
        json="move_down")
    requests.post(f"{API_URL}/api/rooms/testroom/step")
    player = requests.get(f"{API_URL}/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0

    requests.put(
        f"{API_URL}/api/rooms/testroom/agents/{player_id}/setmove",
        json="move_left")
    requests.post(f"{API_URL}/api/rooms/testroom/step")
    player = requests.get(f"{API_URL}/api/rooms/testroom").json()[0]
    assert player["x"] == -1
    assert player["y"] == 0

    requests.put(
        f"{API_URL}/api/rooms/testroom/agents/{player_id}/setmove",
        json="move_right")
    requests.post(f"{API_URL}/api/rooms/testroom/step")
    player = requests.get(f"{API_URL}/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0

    # Don't continue moving
    requests.post(f"{API_URL}/api/rooms/testroom/step")
    player = requests.get(f"{API_URL}/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0
