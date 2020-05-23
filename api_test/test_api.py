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


def same(first, second, strip_id=True):
    """
    Tests if two rooms/views are equal.
    Order doesn't matter, and id is optionally removed.
    """
    if len(first) != len(second):
        return False
    if strip_id:
        first = [{key: entity[key] for key in entity if key != "id"}
                 for entity in first]
        second = [{key: entity[key] for key in entity if key != "id"}
                  for entity in second]
    for entity in first:
        if entity not in second:
            return False
    return True


def test_same_helper():
    assert same(TEST_ROOM, TEST_ROOM)
    assert not same(TEST_ROOM, TEST_ROOM_2)


def test_create_room():
    response = requests.post(f"{API_URL}/api/rooms/", json=TEST_ROOM)
    assert response.status_code == 200
    room_id = response.json()
    # Will throw an exception if it's not a valid UUID
    UUID(hex=room_id)

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
    response = requests.get(f"{API_URL}/api/rooms/testroom/score")
    assert response.status_code == 200
    scores = response.json()
    assert scores[0]["score"] == 0

    requests.post(f"{API_URL}/api/rooms/testroom/step")
    scores = requests.get(f"{API_URL}/api/rooms/testroom/score").json()
    assert scores[0]["score"] != 0


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

    requests.put(
        f"{API_URL}/api/rooms/testroom/agents/{player_id}/setmove",
        json="none")
    requests.post(f"{API_URL}/api/rooms/testroom/step")
    player = requests.get(f"{API_URL}/api/rooms/testroom").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0
