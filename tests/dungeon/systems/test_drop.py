from dungeon.entity import Entity, Inventory, ItemPickup
from dungeon.systems import DropSystem
from dungeon.custom_component_dicts import PositionDict
from dungeon.consts import Drop, Position


def test_drop_item():
    system = DropSystem()
    inventory_components = {
        "a": Inventory(
            items=[Entity(pickup=ItemPickup(
                kind="item"), looksLike="coin")]
        )
    }
    actions = {"a": Drop(index=0)}
    position_components = PositionDict({"a": Position(x=0, y=0)})
    created_entities = system.drop_items(
        inventory_components, actions, position_components
    )
    assert created_entities == [Entity(
        pickup=ItemPickup(kind="item"),
        looksLike="coin",
        position=Position(x=0, y=0)
    )]
    assert len(inventory_components["a"].items) == 0


def test_drop_nonexistent_index_does_nothing():
    system = DropSystem()
    inventory_components = {
        "a": Inventory(
            mode="action",
            items=[Entity(pickup=ItemPickup(
                kind="item"), looksLike="coin")]
        )
    }
    actions = {"a": Drop(index=1)}
    position_components = PositionDict({"a": Position(x=0, y=0)})
    created_entities = system.drop_items(
        inventory_components, actions, position_components
    )
    assert created_entities == []
    assert len(inventory_components["a"].items) == 1
