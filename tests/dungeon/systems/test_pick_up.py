from dungeon.entity import (Pickupper, Inventory, ItemPickup,
                            ScorePickup, VanishPickup)
from dungeon.consts import PickUp, Position
from dungeon.systems import PickUpSystem
from dungeon.custom_component_dicts import PositionDict


def test_pickup_item():
    system = PickUpSystem()
    pickupper_components = {"pickupper": Pickupper(mode="action")}
    inventory_components = {"pickupper": Inventory()}
    actions = {"pickupper": PickUp()}
    position_components = PositionDict({
        "pickupper": Position(x=0, y=0),
        "item": Position(x=0, y=0)
    })
    pickup_components = {"item": ItemPickup(kind="item")}
    score_components = {}
    removed_entities = system.pick_up_items(
        pickupper_components, actions, position_components,
        pickup_components, score_components, inventory_components
    )
    assert inventory_components["pickupper"] == Inventory(items=["item"])
    assert "item" not in position_components
    assert removed_entities == set()


def test_pick_up_item_no_inventory():
    system = PickUpSystem()
    pickupper_components = {"pickupper": Pickupper(mode="action")}
    inventory_components = {}
    actions = {"pickupper": PickUp()}
    position_components = PositionDict({
        "pickupper": Position(x=0, y=0),
        "item": Position(x=0, y=0)
    })
    pickup_components = {"item": ItemPickup(kind="item")}
    score_components = {}
    removed_entities = system.pick_up_items(
        pickupper_components, actions, position_components,
        pickup_components, score_components, inventory_components
    )
    assert "pickupper" not in inventory_components
    assert position_components["item"] == Position(x=0, y=0)
    assert removed_entities == set()


def test_inventory_limit():
    system = PickUpSystem()
    pickupper_components = {"pickupper": Pickupper(mode="action")}
    inventory_components = {
        "pickupper": Inventory(items=["old_item"], limit=1)}
    actions = {"pickupper": PickUp()}
    position_components = PositionDict({
        "pickupper": Position(x=0, y=0),
        "item": Position(x=0, y=0)
    })
    pickup_components = {"item": ItemPickup(kind="item")}
    score_components = {}
    removed_entities = system.pick_up_items(
        pickupper_components, actions, position_components,
        pickup_components, score_components, inventory_components
    )
    assert inventory_components["pickupper"] == Inventory(
        items=["old_item"], limit=1)
    assert position_components["item"] == Position(x=0, y=0)
    assert removed_entities == set()


def test_score_pickup():
    system = PickUpSystem()
    pickupper_components = {"pickupper": Pickupper(mode="action")}
    inventory_components = {}
    actions = {"pickupper": PickUp()}
    position_components = PositionDict({
        "pickupper": Position(x=0, y=0),
        "item": Position(x=0, y=0)
    })
    pickup_components = {"item": ScorePickup(kind="addScore", score=1)}
    score_components = {"pickupper": 3}
    removed_entities = system.pick_up_items(
        pickupper_components, actions, position_components,
        pickup_components, score_components, inventory_components
    )
    assert removed_entities == set(["item"])
    assert score_components["pickupper"] == 4


def test_score_pickup_only_vanish_if_no_score():
    system = PickUpSystem()
    pickupper_components = {"pickupper": Pickupper(mode="action")}
    inventory_components = {}
    actions = {"pickupper": PickUp()}
    position_components = PositionDict({
        "pickupper": Position(x=0, y=0),
        "item": Position(x=0, y=0)
    })
    pickup_components = {"item": ScorePickup(kind="addScore", score=1)}
    score_components = {}
    removed_entities = system.pick_up_items(
        pickupper_components, actions, position_components,
        pickup_components, score_components, inventory_components
    )
    assert removed_entities == set(["item"])
    assert score_components == {}


def test_vanish_pickup():
    system = PickUpSystem()
    pickupper_components = {"pickupper": Pickupper(mode="action")}
    inventory_components = {}
    actions = {"pickupper": PickUp()}
    position_components = PositionDict({
        "pickupper": Position(x=0, y=0),
        "item": Position(x=0, y=0)
    })
    pickup_components = {"item": VanishPickup(kind="vanish")}
    score_components = {}
    removed_entities = system.pick_up_items(
        pickupper_components, actions, position_components,
        pickup_components, score_components, inventory_components
    )
    assert removed_entities == set(["item"])


def test_automatic_pickup():
    system = PickUpSystem()
    pickupper_components = {"pickupper": Pickupper(mode="auto")}
    inventory_components = {}
    actions = {}
    position_components = PositionDict({
        "pickupper": Position(x=0, y=0),
        "item": Position(x=0, y=0)
    })
    pickup_components = {"item": VanishPickup(kind="vanish")}
    score_components = {}
    removed_entities = system.pick_up_items(
        pickupper_components, actions, position_components,
        pickup_components, score_components, inventory_components
    )
    assert removed_entities == set(["item"])
