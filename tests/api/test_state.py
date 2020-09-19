
def test_clear_state(client):
    client.put("/api/templates/testtemplate", json={
        "entities": [
            {"looksLike": "player"}
        ]
    })
    client.post("/api/rooms?from_template=testtemplate")

    response = client.post("/api/state/clear")
    assert response.status_code == 200

    assert client.get("/api/templates").json() == []
    assert client.get("/api/rooms").json() == []
