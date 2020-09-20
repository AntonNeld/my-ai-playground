from uuid import UUID

import yaml

from dungeon.challenge_keeper import Challenge
from dungeon.entity import Entity


def is_uuid(string):
    try:
        UUID(hex=string)
        return True
    except (ValueError, TypeError):
        return False


def room_from_yaml(template):
    challenge = Challenge(**{"template": yaml.safe_load(template)})
    return challenge.create_room()


def test_helper_is_uuid():
    assert is_uuid("9f4118fe668843a3a1c847552a69b1db")
    assert not is_uuid("banana")


def test_helper_room_from_yaml():
    template = """
templateType: "visual"
definitions:
  p:
    ai:
      kind: "singular"
      move: "move_up"
    actions:
      move_up: {}
      move_down: {}
room: |-
  p
"""
    room = room_from_yaml(template)
    assert room.get_entities() == [Entity(**{
        "position": {
            "x": 0,
            "y": 0
        },
        "ai": {
            "kind": "singular",
            "move": "move_up"
        },
        "actions": {
            "move_up": {},
            "move_down": {}
        }
    })]
