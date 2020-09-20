from pathlib import Path

import pytest

from dungeon.challenge_keeper import (ChallengeKeeper, challenge_from_txt,
                                      Challenge, ParseError)
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

PARSED_TEXT_CHALLENGE = Challenge(**{
    "template": {
        "templateType": "visual",
        "definitions": {
            "p": {
                "looksLike": "player"
            },
            "c": {"looksLike": "coin"},
            "#": {"looksLike": "wall"}
        },
        "room": " #\npc"
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


def test_load_txt(loaded_keeper):
    challenge = loaded_keeper.get_challenge("txt_example")
    assert challenge == PARSED_TEXT_CHALLENGE


def test_parse_ignore_comment():
    challenge = challenge_from_txt("""
// This is a comment
{
  "definitions": {
    // This is a comment inside the JSON
    "p": {"looksLike": "player"}
  }
}

p

""")
    assert challenge.create_room().get_entities() == [
        Entity(**{"looksLike": "player", "position": {"x": 0, "y": 0}})]


def test_parse_colocated_entities():
    challenge = challenge_from_txt("""
{
  "definitions": {
    "a": [{"looksLike": "player"}, {"looksLike": "wall"}]
  }
}

a

""")
    entities = challenge.create_room().get_entities()
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "player"}) in entities
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "wall"}) in entities


def test_parse_colocated_entities_with_refs():
    challenge = challenge_from_txt("""
{
  "definitions": {
    "a": [{"looksLike": "player"}, "#"],
    "#": {"looksLike": "wall"}
  }
}

a

""")
    entities = challenge.create_room().get_entities()
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "player"}) in entities
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "wall"}) in entities


def test_parse_nested_refs():
    challenge = challenge_from_txt("""
{
  "definitions": {
    "a": ["b"],
    "b": "c",
    "c": {"looksLike": "coin"}
  }
}

a

""")
    assert challenge.create_room().get_entities() == [
        Entity(**{"looksLike": "coin", "position": {"x": 0, "y": 0}})]


def test_parse_circular_refs():
    challenge = challenge_from_txt("""
{
  "definitions": {
    "a": "b",
    "b": "c",
    "c": "a"
  }
}

a

""")
    with pytest.raises(ParseError):
        challenge.create_room()


def test_challenge_not_modified_by_room():
    challenge = Challenge(
        **{"template":
           {"templateType": "raw",
            "entities": [
                {"position": {"x": 0, "y": 0}, "looksLike": "player"},
            ]
            }
           })
    room = challenge.create_room()
    room.get_entities()[0].position.x = 1
    assert challenge.template.entities[0].position.x == 0
