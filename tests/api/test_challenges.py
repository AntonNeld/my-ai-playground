def test_get_variants(client):
    client.put("/api/challenges/testchallenge", json={
        "variants": {
            "variantOne": {
                "entities[0].looksLike": "coin"
            },
            "variantTwo": {}
        },
        "template": {
            "templateType": "raw",
            "entities": [{"looksLike": "wall"}]
        }
    })
    response = client.get("/api/challenges/testchallenge/variants")
    assert response.status_code == 200
    assert response.json() == ["variantOne", "variantTwo"]


def test_get_no_variants(client):
    client.put("/api/challenges/testchallenge", json={
        "template": {
            "templateType": "raw",
            "entities": [{"looksLike": "wall"}]
        }
    })
    response = client.get("/api/challenges/testchallenge/variants")
    assert response.status_code == 200
    assert response.json() == []
