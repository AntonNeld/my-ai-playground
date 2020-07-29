import pytest


@pytest.mark.parametrize("method", ["post", "put"])
def test_create_room_from_template(client, method):
    client.put("/api/templates/testtemplate", json={
        "entities": [{"x": 0, "y": 0, "looksLike": "wall"}]
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
    assert len(room["entities"]) == 1
    assert {"x": 0, "y": 0, "looksLike": "wall"} in room["entities"].values()
    assert room["steps"] == 0


@pytest.mark.parametrize("method", ["post", "put"])
def test_body_required_if_no_template(client, method):
    if method == "post":
        response = client.post("/api/rooms")
    elif method == "put":
        response = client.put(
            "/api/rooms/testroom")
    assert response.status_code == 422


@pytest.mark.parametrize("steps", [None, 1, 10])
def test_step(client, steps):
    client.put("/api/rooms/testroom", json={
        "steps": 0,
        "entities": {}
    })

    response = client.post(
        "/api/rooms/testroom/step" if steps is None
        else f"/api/rooms/testroom/step?steps={steps}")
    assert response.status_code == 200

    room_after = client.get("/api/rooms/testroom").json()
    assert room_after == {
        "steps": 1 if steps is None else steps,
        "entities": {}
    }
