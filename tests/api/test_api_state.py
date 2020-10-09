
def test_clear_state(client):
    client.put("/api/challenges/testchallenge", json={
        "template": {
            "templateType": "raw",
            "entities": [
                {"looksLike": "player"}
            ]
        }})
    client.post("/api/rooms?from_challenge=testchallenge")

    response = client.post("/api/state/clear")
    assert response.status_code == 200

    assert client.get("/api/challenges").json() == []
    assert client.get("/api/rooms").json() == []
