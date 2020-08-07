def test_evaluate(client):
    response = client.put("/api/templates/testtemplate", json={
        "entities": [
            {
                "label": "entityOne",
                "pickupper": {"inventory": [{}]},
                "scoring": {"kind": "heldItems"}
            },
            {
                "label": "entityTwo",
                "score": 0
            },
        ]
    })

    response = client.post(
        "/api/evaluate", json={"template": "testtemplate", "duration": 3})
    assert response.status_code == 200
    assert response.json() == {"entityOne": 1, "entityTwo": 0}
