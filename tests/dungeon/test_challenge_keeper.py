from pathlib import Path

import pytest

from dungeon.challenge_keeper import ChallengeKeeper, Challenge
from dungeon.entity import Entity

PARENT_DIR = Path(__file__).parent

RAW_CHALLENGE = Challenge(**{
    "template": {
        "templateType": "raw",
        "entities": [
            {"position": {"x": 0, "y": 0}, "looksLike": "player"},
            {"position": {"x": 1, "y": 1}, "looksLike": "wall"},
            {"position": {"x": 1, "y": 0}, "looksLike": "coin"}
        ]
    }
})


@pytest.fixture
def loaded_keeper():
    challenge_keeper = ChallengeKeeper()
    challenge_keeper.load_directory(
        PARENT_DIR / "test_challenge_keeper" / "challenges")
    return challenge_keeper


def test_load_json(loaded_keeper):
    challenge = loaded_keeper.get_challenge("json_example")
    assert challenge == RAW_CHALLENGE


def test_load_yaml(loaded_keeper):
    challenge = loaded_keeper.get_challenge("yaml_example")
    assert challenge == RAW_CHALLENGE


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
