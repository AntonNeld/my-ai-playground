import pytest
import random

from dungeon.components import (Pickupper, Inventory, ItemPickup,
                                ScorePickup, VanishPickup)
from dungeon.actions import PickUp
from dungeon.components import Position
from dungeon.systems import PickUpSystem
from dungeon.custom_component_dicts import PositionDict
from test_utils import MockRandom


def test_pickup_item():
    system = PickUpSystem()
    random_generator = random.Random(123)
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
        pickup_components, score_components, inventory_components,
        random_generator
    )
    assert inventory_components["pickupper"] == Inventory(items=["item"])
    assert "item" not in position_components
    assert removed_entities == set()


def test_pick_up_item_no_inventory():
    system = PickUpSystem()
    random_generator = random.Random(123)
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
        pickup_components, score_components, inventory_components,
        random_generator
    )
    assert "pickupper" not in inventory_components
    assert position_components["item"] == Position(x=0, y=0)
    assert removed_entities == set()


def test_inventory_limit():
    system = PickUpSystem()
    random_generator = random.Random(123)
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
        pickup_components, score_components, inventory_components,
        random_generator
    )
    assert inventory_components["pickupper"] == Inventory(
        items=["old_item"], limit=1)
    assert position_components["item"] == Position(x=0, y=0)
    assert removed_entities == set()


def test_score_pickup():
    system = PickUpSystem()
    random_generator = random.Random(123)
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
        pickup_components, score_components, inventory_components,
        random_generator
    )
    assert removed_entities == set(["item"])
    assert score_components["pickupper"] == 4


def test_score_pickup_only_vanish_if_no_score():
    system = PickUpSystem()
    random_generator = random.Random(123)
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
        pickup_components, score_components, inventory_components,
        random_generator
    )
    assert removed_entities == set(["item"])
    assert score_components == {}


def test_vanish_pickup():
    system = PickUpSystem()
    random_generator = random.Random(123)
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
        pickup_components, score_components, inventory_components,
        random_generator
    )
    assert removed_entities == set(["item"])


def test_automatic_pickup():
    system = PickUpSystem()
    random_generator = random.Random(123)
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
        pickup_components, score_components, inventory_components,
        random_generator
    )
    assert removed_entities == set(["item"])


@pytest.mark.parametrize("chosen", ["a", "b", "c"])
def test_many_tries_pickup_winner_selected_randomly(chosen):
    system = PickUpSystem()
    random_generator = MockRandom(chosen)
    pickupper_components = {
        "a": Pickupper(mode="action"),
        "b": Pickupper(mode="action"),
        "c": Pickupper(mode="action")
    }
    actions = {"a": PickUp(), "b": PickUp(), "c": PickUp()}
    position_components = PositionDict({
        "a": Position(x=0, y=0),
        "b": Position(x=0, y=0),
        "c": Position(x=0, y=0),
        "item": Position(x=0, y=0)
    })
    pickup_components = {"item": ScorePickup(kind="addScore", score=1)}
    score_components = {
        "a": 0,
        "b": 0,
        "c": 0
    }
    inventory_components = {}

    system.pick_up_items(
        pickupper_components, actions, position_components,
        pickup_components, score_components, inventory_components,
        random_generator
    )
    assert score_components[chosen] == 1
    for entity_id in ("a", "b", "c"):
        if entity_id != chosen:
            assert score_components[entity_id] == 0
