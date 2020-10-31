from dungeon.components import Inventory
from dungeon.systems import DropSystem
from dungeon.custom_component_dicts import PositionDict
from dungeon.actions import Drop
from dungeon.components import Position


def test_drop_item():
    system = DropSystem()
    inventory_components = {
        "a": Inventory(
            items=["item"]
        )
    }
    actions = {"a": Drop(index=0)}
    position_components = PositionDict({"a": Position(x=0, y=0)})
    system.drop_items(inventory_components, actions, position_components)
    assert position_components["item"] == Position(x=0, y=0)
    assert len(inventory_components["a"].items) == 0


def test_drop_nonexistent_index_does_nothing():
    system = DropSystem()
    inventory_components = {
        "a": Inventory(
            mode="action",
            items=["item"]
        )
    }
    actions = {"a": Drop(index=1)}
    position_components = PositionDict({"a": Position(x=0, y=0)})
    system.drop_items(inventory_components, actions, position_components)
    assert "item" not in position_components
    assert len(inventory_components["a"].items) == 1
