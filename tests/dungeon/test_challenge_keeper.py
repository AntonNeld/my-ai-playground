from dungeon.challenge_keeper import Challenge
from dungeon.entity import Entity


def test_create_room_with_none_variant():
    challenge = Challenge(**{
        "variants": {
            "variantOne": {
                "definitions.p.looksLike": "wall",
                "definitions.q.looksLike": "wall",
            }
        },
        "template": {
            "templateType": "visual",
            "definitions": {
                "p": {"looksLike": "player"},
                "c": {"looksLike": "coin"},
            },
            "room": "pc"
        }
    })
    entities = challenge.create_room().get_entities()
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "player"}) in entities
    assert Entity(**{"position": {"x": 1, "y": 0},
                     "looksLike": "coin"}) in entities


def test_create_room_with_variant():
    challenge = Challenge(**{
        "variants": {
            "variantOne": {
                "definitions.p.looksLike": "wall",
                "definitions.c.looksLike": "wall",
            }
        },
        "template": {
            "templateType": "visual",
            "definitions": {
                "p": {"looksLike": "player"},
                "c": {"looksLike": "coin"},
            },
            "room": "pc"
        }
    })
    entities = challenge.create_room(variant="variantOne").get_entities()
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "wall"}) in entities
    assert Entity(**{"position": {"x": 1, "y": 0},
                     "looksLike": "wall"}) in entities
