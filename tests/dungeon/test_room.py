import pytest

from test_utils import room_from_yaml
from dungeon.entity import Entity
from dungeon.consts import PickUp


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


def test_attack():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      action:
        actionType: "attack"
        direction: "right"
    actions:
      attack: {}
  e:
    vulnerable: {}
  "#": {}
room: |-
 #pe
""")

    room.step()
    assert len(room.get_entities()) == 2
    room.step()
    assert len(room.get_entities()) == 2
    room.get_entities(looks_like="player")[0].ai.action.direction = "left"
    room.step()
    assert len(room.get_entities()) == 2


def test_pickup():
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
    pickupper: {}
    actions:
      move: {}
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
      action:
        actionType: "move"
        direction: "right"
    pickupper:
      inventoryLimit: 1
    actions:
      move: {}
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
      action:
        actionType: "move"
        direction: "right"
    pickupper:
      mode: "action"
    actions:
      move: {}
      pick_up: {}
  c:
    pickup:
      kind: "item"
room: |-
  pc
""")

    room.step()
    assert len(room.get_entities()) == 2
    room.get_entities(looks_like="player")[0].ai.action = PickUp()
    room.step()
    assert len(room.get_entities()) == 1
    assert room.get_entities()[0].pickupper.inventory == [
        Entity(**{"pickup": {"kind": "item"}})]


def test_drop():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      action:
        actionType: "drop"
        index: 1
    pickupper:
      mode: "action"
      inventory:
        - looksLike: "coin"
          pickup:
            kind: "item"
        - looksLike: "evilCoin"
          pickup:
            kind: "item"
            providesTags:
              - "evil"
    actions:
      drop: {}
room: |-
  p
""")

    room.step()
    assert len(room.get_entities()) == 2
    assert room.get_entities(looks_like="player")[0].pickupper.inventory == [
        Entity(**{"looksLike": "coin", "pickup": {"kind": "item"}})]
    assert not room.get_entities(looks_like="player")[0].get_tags()
    room.step()
    assert len(room.get_entities()) == 2
    assert room.get_entities(looks_like="player")[0].pickupper.inventory == [
        Entity(**{"looksLike": "coin", "pickup": {"kind": "item"}})]


def test_drop_autopickup():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      action:
        actionType: "drop"
    pickupper:
      mode: "auto"
      inventory:
        - pickup:
            kind: "item"
    actions:
      drop: {}
room: |-
  p
""")
    room.step()
    assert len(room.get_entities()) == 2


def test_score_pickup():
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
    score: 0
    pickupper: {}
    actions:
      move: {}
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
      action:
        actionType: "move"
        direction: "right"
    pickupper: {}
    actions:
      move: {}
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
      action:
        actionType: "move"
        direction: "right"
    pickupper: {}
    actions:
      move: {}
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
      action:
        actionType: "move"
        direction: "right"
    pickupper: {}
    actions:
      move: {}
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

    room.step()
    player = room.get_entities(label="player")[0]
    assert player.score == 2
    room.step()
    player = room.get_entities(label="player")[0]
    assert player.score == 4


def test_move_penalty():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    label: "player"
    ai:
      kind: "singular"
      action:
        actionType: "move"
        direction: "right"
    actions:
      move:
        cost: 1
    score: 0
  "#":
    blocksMovement: {}
room: |-
  p#
""")

    room.step()
    assert room.get_entities(label="player")[0].score == -1
