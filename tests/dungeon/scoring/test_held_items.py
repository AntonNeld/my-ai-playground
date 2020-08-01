import pytest

from test_utils import room_from_text


def test_score_0_no_can_pickup():
    room = room_from_text("""
{
  "definitions": {
    "p": {"scoring": {"kind": "heldItems"}}
  }
}

p
    """)
    entity = room.get_entities()[0]
    assert entity.scoring.get_score(entity, room) == 0


@pytest.mark.parametrize("items", [0, 1, 10])
def test_score_inventory_length(items):
    room = room_from_text("""
{
  "definitions": {
    "p": {"canPickup": {"inventory": []}, "scoring": {"kind": "heldItems"}}
  }
}

p
    """)
    entity = room.get_entities()[0]
    entity.can_pickup.inventory += [{}] * items
    assert entity.scoring.get_score(entity, room) == items
