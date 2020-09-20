import pytest

from test_utils import room_from_yaml


def test_score_0_no_pickupper():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    scoring:
      kind: "heldItems"
room: |-
  p
""")

    entity = room.get_entities()[0]
    assert entity.scoring.get_score(entity, room) == 0


@pytest.mark.parametrize("items", [0, 1, 10])
def test_score_inventory_length(items):
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    pickupper:
      inventory: []
    scoring:
      kind: "heldItems"
room: |-
  p
""")

    entity = room.get_entities()[0]
    entity.pickupper.inventory += [{}] * items
    assert entity.scoring.get_score(entity, room) == items
