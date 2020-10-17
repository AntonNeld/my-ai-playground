from test_utils import room_from_yaml
from dungeon.entity import Entity


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
    actions:
      drop: {}
room: |-
  p
""")

    room.step()
    assert len(room.get_entities()) == 2
    assert room.get_entities(looks_like="player")[0].pickupper.inventory == [
        Entity(**{"looksLike": "coin", "pickup": {"kind": "item"}})]
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
