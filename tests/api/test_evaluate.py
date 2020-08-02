def test_evaluate(client):
    response = client.put("/api/templates/testtemplate", json={
        "entities": [
            {
                "label": "entityOne",
                "pickupper": {"inventory": [{}]},
                "scoring": {"kind": "heldItems"},
                "cumulativeScore": 0
            },
            {
                "label": "entityTwo",
                "scoring": {"kind": "heldItems"}
            },
        ]
    })

    response = client.post(
        "/api/evaluate", json={"template": "testtemplate", "duration": 3})
    assert response.status_code == 200
    assert response.json() == {"entityOne": 3, "entityTwo": 0}
