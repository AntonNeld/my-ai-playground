import pytest

from test_utils import room_from_yaml


@pytest.mark.parametrize("direction,x,y",
                         [("up", 0, 1), ("down", 0, -1),
                          ("left", -1, 0), ("right", 1, 0)])
def test_action_move(direction, x, y):
    room = room_from_yaml(f"""
templateType: "visual"
definitions:
  p:
    ai:
      kind: "singular"
      action:
        actionType: "move"
        direction: "{direction}"
    actions:
      move: {{}}
room: |-
  p
""")

    room.step()
    assert room.get_entities()[0].position.x == x
    assert room.get_entities()[0].position.y == y


def test_blocks_movement():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      action:
        actionType: "move"
        direction: "right"
    actions:
      move: {}
  "#":
    blocksMovement: {}
room: |-
  p#
""")

    room.step()
    assert room.get_entities(looks_like="player")[0].position.x == 0


def test_blocks_movement_wrong_tags():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      action:
        actionType: "move"
        direction: "right"
    actions:
      move: {}
  "~":
    blocksMovement:
      passableForTags:
        - "pass"
room: |-
  p~
""")

    room.step()
    assert room.get_entities(looks_like="player")[0].position.x == 0


def test_blocks_movement_right_tags():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      action:
        actionType: "move"
        direction: "right"
    tags:
      - "pass"
    actions:
      move: {}
  "~":
    blocksMovement:
      passableForTags:
        - "pass"
room: |-
  p~
""")

    room.step()
    assert room.get_entities(looks_like="player")[0].position.x == 1
