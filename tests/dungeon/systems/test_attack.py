from test_utils import room_from_yaml


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
