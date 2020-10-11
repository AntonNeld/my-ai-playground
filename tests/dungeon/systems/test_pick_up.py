from test_utils import room_from_yaml
from dungeon.entity import Entity
from dungeon.consts import PickUp


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
