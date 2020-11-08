import pytest

from dungeon.systems import MovementSystem
from dungeon.actions import Move
from dungeon.components import Position, BlocksMovement, Swappable
from dungeon.custom_component_dicts import PositionDict


@pytest.mark.parametrize("direction,x,y",
                         [("up", 0, 1), ("down", 0, -1),
                          ("left", -1, 0), ("right", 1, 0)])
def test_move_direction(direction, x, y):
    system = MovementSystem()
    actions = {"a": Move(direction=direction)}
    position_components = PositionDict({"a": Position(x=0, y=0)})
    blocks_movement_components = {}
    tags = {}
    swappable_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags,
                         swappable_components)
    assert position_components["a"] == Position(x=x, y=y)


def test_blocks_movement():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {"b": BlocksMovement()}
    tags = {}
    swappable_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags,
                         swappable_components)
    assert position_components["a"] == Position(x=0, y=0)


def test_blocks_movement_wrong_tags():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {
        "b": BlocksMovement(passableForTags=["pass"])}
    tags = {"a": ["notPass"]}
    swappable_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags,
                         swappable_components)
    assert position_components["a"] == Position(x=0, y=0)


def test_blocks_movement_right_tags():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {
        "b": BlocksMovement(passableForTags=["pass"])}
    tags = {"a": ["pass"]}
    swappable_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags,
                         swappable_components)
    assert position_components["a"] == Position(x=1, y=0)


def test_blocker_cannot_move_into_others_space():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {"a": BlocksMovement()}
    tags = {}
    swappable_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags,
                         swappable_components)
    assert position_components["a"] == Position(x=0, y=0)


def test_swap():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {}
    tags = {}
    swappable_components = {"b": Swappable()}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags,
                         swappable_components)
    assert position_components["a"] == Position(x=1, y=0)
    assert position_components["b"] == Position(x=0, y=0)


def test_cannot_swap_blockers():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {"b": BlocksMovement()}
    tags = {}
    swappable_components = {"b": Swappable()}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags,
                         swappable_components)
    assert position_components["a"] == Position(x=0, y=0)
    assert position_components["b"] == Position(x=1, y=0)


def test_cannot_swap_if_other_entity_is_blocked():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict({
        "a": Position(x=0, y=0),
        "b": Position(x=1, y=0),
        "c": Position(x=0, y=0)
    })
    blocks_movement_components = {
        "c": BlocksMovement(passableForTags=["pass"])}
    tags = {"a": ["pass"]}
    swappable_components = {"b": Swappable()}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags,
                         swappable_components)
    assert position_components["a"] == Position(x=0, y=0)
    assert position_components["b"] == Position(x=1, y=0)
