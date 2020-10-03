import pytest

from test_utils import room_from_yaml
from dungeon.entity import Entity


@pytest.mark.parametrize("move,x,y",
                         [("move_up", 0, 1), ("move_down", 0, -1),
                          ("move_left", -1, 0), ("move_right", 1, 0)])
def test_action_move(move, x, y):
    room = room_from_yaml(f"""
templateType: "visual"
definitions:
  p:
    ai:
      kind: "singular"
      move: "{move}"
    actions:
      move_up: {{}}
      move_down: {{}}
      move_left: {{}}
      move_right: {{}}
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
      move: "move_right"
    actions:
      move_right: {}
  "#":
    blocksMovement: {}
room: |-
  p#
""")

    room.step()
    assert room.get_entities(looks_like="player")[0].position.x == 0


def test_blocks_movement_except_tags():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      move: "move_right"
    actions:
      move_right: {}
  "~":
    blocksMovement:
      passableForTags:
        - "pass"
room: |-
  p~
""")

    room.step()
    assert room.get_entities(looks_like="player")[0].position.x == 0
    room.get_entities(looks_like="player")[0].tags = ["pass"]
    room.step()
    assert room.get_entities(looks_like="player")[0].position.x == 1


def test_pickup():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      move: "move_right"
    pickupper: {}
    actions:
      move_right: {}
  c:
    pickup:
      kind: "item"
room: |-
  pc
""")

    room.step()
    assert len(room.get_entities()) == 1
    assert room.get_entities()[0].pickupper.inventory == [
        Entity(**{"pickup": {"kind": "item"}})]


def test_inventory_limit():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      move: "move_right"
    pickupper:
      inventoryLimit: 1
    actions:
      move_right: {}
  c:
    pickup:
      kind: "item"
room: |-
  pcc
""")

    room.step()
    assert len(room.get_entities()) == 2
    assert room.get_entities(looks_like="player")[0].pickupper.inventory == [
        Entity(**{"pickup": {"kind": "item"}})]
    room.step()
    assert len(room.get_entities()) == 2
    assert room.get_entities(looks_like="player")[0].pickupper.inventory == [
        Entity(**{"pickup": {"kind": "item"}})]


def test_pickup_action():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      move: "move_right"
    pickupper:
      mode: "action"
    actions:
      move_right: {}
      pick_up: {}
  c:
    pickup:
      kind: "item"
room: |-
  pc
""")

    room.step()
    assert len(room.get_entities()) == 2
    room.get_entities(looks_like="player")[0].ai.move = "pick_up"
    room.step()
    assert len(room.get_entities()) == 1
    assert room.get_entities()[0].pickupper.inventory == [
        Entity(**{"pickup": {"kind": "item"}})]


def test_score_pickup():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      move: "move_right"
    score: 0
    pickupper: {}
    actions:
      move_right: {}
  c:
    pickup:
      kind: "addScore"
      score: 2
room: |-
  pc
""")

    room.step()
    assert len(room.get_entities()) == 1
    assert room.get_entities()[0].score == 2


def test_score_pickup_score_none():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      move: "move_right"
    pickupper: {}
    actions:
      move_right: {}
  c:
    pickup:
      kind: "addScore"
      score: 2
room: |-
  pc
""")

    room.step()
    assert len(room.get_entities()) == 1
    assert room.get_entities()[0].score is None


def test_vanish_pickup():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      move: "move_right"
    pickupper: {}
    actions:
      move_right: {}
  c:
    pickup:
      kind: "vanish"
room: |-
  pc
""")

    room.step()
    assert len(room.get_entities()) == 1
    assert room.get_entities()[0].pickupper.inventory == []


def test_item_provides_tags():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      move: "move_right"
    pickupper: {}
    actions:
      move_right: {}
    tags:
      - "tagZero"
  c:
    pickup:
      kind: "item"
      providesTags:
        - "tagOne"
        - "tagTwo"
room: |-
  pc
""")
    room.step()
    tags = room.get_entities(looks_like="player")[0].get_tags()
    assert "tagZero" in tags
    assert "tagOne" in tags
    assert "tagTwo" in tags


def test_get_view():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    perception: {}
  c:
    looksLike: "coin"
  "#":
    looksLike: "wall"
room: |-2
     #
  p  c
""")

    perceptor = room.get_entities(looks_like="player")[0]
    entities = room.get_view(perceptor)["entities"]
    assert len(entities) == 2
    assert {"x": 3, "y": 0, "looks_like": "coin"} in entities
    assert {"x": 3, "y": 1, "looks_like": "wall"} in entities


def test_get_view_with_max_distance():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    perception:
      distance: 3
  c:
    looksLike: "coin"
  "#":
    looksLike: "wall"
room: |-
  #     #
     p  c
  #     #
""")

    perceptor = room.get_entities(looks_like="player")[0]
    entities = room.get_view(perceptor)["entities"]
    assert len(entities) == 1
    assert {"x": 3, "y": 0, "looks_like": "coin"} in entities


def test_get_view_with_position():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    perception:
      includePosition: true
  "#":
    looksLike: "wall"
room: |-2
     #
  # p
""")

    perceptor = room.get_entities(looks_like="player")[0]
    position = room.get_view(perceptor)["position"]
    assert position["x"] == 2
    assert position["y"] == 0


def test_count_tags_score():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    label: "player"
    score: 0
  d:
    tags:
      - "dirt"
  ".":
    countTagsScore:
      addTo: "player"
      score: 1
      tags:
        dirt: 0
  a:
    - "d"
    - "."
room: |-
  p  a..
""")

    player = room.get_entities(label="player")[0]
    room.step()
    assert player.score == 2
    room.step()
    assert player.score == 4


def test_move_penalty():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    label: "player"
    ai:
      kind: "singular"
      move: "move_right"
    actions:
      move_right:
        cost: 1
    score: 0
  "#":
    blocksMovement: {}
room: |-
  p#
""")

    room.step()
    assert room.get_entities(label="player")[0].score == -1
