from uuid import UUID

import requests

API_URL = "http://localhost:8300"

TEST_ROOM = [
    {"x": 0, "y": 0, "type": "player", "ai": "pathfinder"},
    {"x": 1, "y": 1, "type": "block"},
    {"x": 1, "y": 0, "type": "coin"}
]

TEST_ROOM_VIEW = [
    {"x": 0, "y": 0, "looks_like": "player"},
    {"x": 1, "y": 1, "looks_like": "wall"},
    {"x": 1, "y": 0, "looks_like": "coin"}
]

TEST_ROOM_2 = [
    {"x": 0, "y": 0, "type": "player", "ai": "manual"}
]

TEST_ROOM_2_VIEW = [
    {"x": 0, "y": 0, "looks_like": "player"}
]


def same_view(first, second, strip_id=True):
    """
    Tests if two views are equal.
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


def test_same_view():
    assert same_view(TEST_ROOM_VIEW, TEST_ROOM_VIEW)
    assert not same_view(TEST_ROOM_VIEW, TEST_ROOM_2_VIEW)


def test_create_room():
    response = requests.post(f"{API_URL}/api/room/", json=TEST_ROOM)
    assert response.status_code == 200
    room_id = response.json()
    # Check that it's a valid UUID
    UUID(hex=room_id)

    response = requests.get(f"{API_URL}/api/room/{room_id}/view")
    assert same_view(response.json(), TEST_ROOM_VIEW)


def test_create_two_rooms():
    room_id = requests.post(f"{API_URL}/api/room/", json=TEST_ROOM).json()
    room_id_2 = requests.post(f"{API_URL}/api/room/", json=TEST_ROOM_2).json()
    room_1 = requests.get(f"{API_URL}/api/room/{room_id}/view").json()
    room_2 = requests.get(f"{API_URL}/api/room/{room_id_2}/view").json()
    assert same_view(room_1, TEST_ROOM_VIEW)
    assert same_view(room_2, TEST_ROOM_2_VIEW)


def test_replace_room():
    requests.post(f"{API_URL}/api/room/testroom", json=TEST_ROOM)
    room_1 = requests.get(f"{API_URL}/api/room/testroom/view").json()
    assert same_view(room_1, TEST_ROOM_VIEW)

    requests.post(f"{API_URL}/api/room/testroom", json=TEST_ROOM_2)
    room_2 = requests.get(f"{API_URL}/api/room/testroom/view").json()
    assert same_view(room_2, TEST_ROOM_2_VIEW)


def test_delete_room():
    requests.post(f"{API_URL}/api/room/testroom", json=TEST_ROOM)
    response = requests.delete(f"{API_URL}/api/room/testroom")
    assert response.status_code == 200
    response = requests.get(f"{API_URL}/api/room/testroom/view")
    assert response.status_code == 500  # TODO: Fix to 404


def test_step():
    requests.post(f"{API_URL}/api/room/testroom", json=TEST_ROOM)
    room_before = requests.get(f"{API_URL}/api/room/testroom/view").json()

    response = requests.post(f"{API_URL}/api/room/testroom/step")
    assert response.status_code == 200

    room_after = requests.get(f"{API_URL}/api/room/testroom/view").json()
    assert not same_view(room_before, room_after)


def test_get_step():
    requests.post(f"{API_URL}/api/room/testroom", json=TEST_ROOM)
    response = requests.get(f"{API_URL}/api/room/testroom/step")
    assert response.status_code == 200
    step = response.json()
    assert step == 0

    requests.post(f"{API_URL}/api/room/testroom/step")
    step = requests.get(f"{API_URL}/api/room/testroom/step").json()
    assert step == 1


def test_score():
    requests.post(f"{API_URL}/api/room/testroom", json=TEST_ROOM)
    response = requests.get(f"{API_URL}/api/room/testroom/score")
    assert response.status_code == 200
    scores = response.json()
    assert scores[0]["score"] == 0

    requests.post(f"{API_URL}/api/room/testroom/step")
    scores = requests.get(f"{API_URL}/api/room/testroom/score").json()
    assert scores[0]["score"] != 0


def test_manual_ai():
    requests.post(f"{API_URL}/api/room/testroom", json=TEST_ROOM_2)
    player = requests.get(f"{API_URL}/api/room/testroom/view").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0
    player_id = player["id"]

    requests.put(
        f"{API_URL}/api/room/testroom/agent/{player_id}/setmove",
        json="move_up")
    requests.post(f"{API_URL}/api/room/testroom/step")
    player = requests.get(f"{API_URL}/api/room/testroom/view").json()[0]
    assert player["x"] == 0
    assert player["y"] == 1

    requests.put(
        f"{API_URL}/api/room/testroom/agent/{player_id}/setmove",
        json="move_down")
    requests.post(f"{API_URL}/api/room/testroom/step")
    player = requests.get(f"{API_URL}/api/room/testroom/view").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0

    requests.put(
        f"{API_URL}/api/room/testroom/agent/{player_id}/setmove",
        json="move_left")
    requests.post(f"{API_URL}/api/room/testroom/step")
    player = requests.get(f"{API_URL}/api/room/testroom/view").json()[0]
    assert player["x"] == -1
    assert player["y"] == 0

    requests.put(
        f"{API_URL}/api/room/testroom/agent/{player_id}/setmove",
        json="move_right")
    requests.post(f"{API_URL}/api/room/testroom/step")
    player = requests.get(f"{API_URL}/api/room/testroom/view").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0

    requests.put(
        f"{API_URL}/api/room/testroom/agent/{player_id}/setmove",
        json="none")
    requests.post(f"{API_URL}/api/room/testroom/step")
    player = requests.get(f"{API_URL}/api/room/testroom/view").json()[0]
    assert player["x"] == 0
    assert player["y"] == 0
