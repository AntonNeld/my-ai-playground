from test_utils import room_from_yaml


def test_action_penalty():
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
