from dungeon.entity import Entity, Pickupper, ItemPickup
from dungeon.systems import DropSystem
from dungeon.custom_component_dicts import PositionDict
from dungeon.consts import Drop, Position


def test_drop_item():
    system = DropSystem()
    pickupper_components = {
        "a": Pickupper(
            mode="action",
            inventory=[Entity(pickup=ItemPickup(
                kind="item"), looksLike="coin")]
        )
    }
    actions = {"a": Drop(index=0)}
    position_components = PositionDict({"a": Position(x=0, y=0)})
    created_entities = system.drop_items(
        pickupper_components, actions, position_components
    )
    assert created_entities == [Entity(
        pickup=ItemPickup(kind="item"),
        looksLike="coin",
        position=Position(x=0, y=0)
    )]
    assert len(pickupper_components["a"].inventory) == 0


def test_drop_nonexistent_index_does_nothing():
    system = DropSystem()
    pickupper_components = {
        "a": Pickupper(
            mode="action",
            inventory=[Entity(pickup=ItemPickup(
                kind="item"), looksLike="coin")]
        )
    }
    actions = {"a": Drop(index=1)}
    position_components = PositionDict({"a": Position(x=0, y=0)})
    created_entities = system.drop_items(
        pickupper_components, actions, position_components
    )
    assert created_entities == []
    assert len(pickupper_components["a"].inventory) == 1
