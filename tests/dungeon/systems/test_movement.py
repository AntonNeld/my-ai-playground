import pytest

from dungeon.systems import MovementSystem
from dungeon.actions import Move, Swap
from dungeon.components import Position
from dungeon.custom_component_dicts import PositionDict
from dungeon.components import BlocksMovement


@pytest.mark.parametrize("direction,x,y",
                         [("up", 0, 1), ("down", 0, -1),
                          ("left", -1, 0), ("right", 1, 0)])
def test_move_direction(direction, x, y):
    system = MovementSystem()
    actions = {"a": Move(direction=direction)}
    position_components = PositionDict({"a": Position(x=0, y=0)})
    blocks_movement_components = {}
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components)
    assert position_components["a"] == Position(x=x, y=y)


def test_blocks_movement():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {"b": BlocksMovement()}
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components)
    assert position_components["a"] == Position(x=0, y=0)


def test_blocks_movement_wrong_tags():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {
        "b": BlocksMovement(passableForTags=["pass"])}
    tags_components = {"a": ["notPass"]}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components)
    assert position_components["a"] == Position(x=0, y=0)


def test_blocks_movement_right_tags():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {
        "b": BlocksMovement(passableForTags=["pass"])}
    tags_components = {"a": ["pass"]}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components)
    assert position_components["a"] == Position(x=1, y=0)


def test_blocker_cannot_move_into_others_space():
    system = MovementSystem()
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {"a": BlocksMovement()}
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components)
    assert position_components["a"] == Position(x=0, y=0)


@pytest.mark.parametrize("direction,x,y",
                         [("up", 0, 1), ("down", 0, -1),
                          ("left", -1, 0), ("right", 1, 0)])
def test_swap_direction(direction, x, y):
    system = MovementSystem()
    actions = {"a": Swap(direction=direction)}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=x, y=y)})
    blocks_movement_components = {}
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components)
    assert position_components["a"] == Position(x=x, y=y)
    assert position_components["b"] == Position(x=0, y=0)


def test_cannot_swap_blockers():
    system = MovementSystem()
    actions = {"a": Swap(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {"b": BlocksMovement()}
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components)
    assert position_components["a"] == Position(x=0, y=0)
    assert position_components["b"] == Position(x=1, y=0)


def test_cannot_swap_if_other_entity_is_blocked():
    system = MovementSystem()
    actions = {"a": Swap(direction="right")}
    position_components = PositionDict({
        "a": Position(x=0, y=0),
        "b": Position(x=1, y=0),
        "c": Position(x=0, y=0)
    })
    blocks_movement_components = {
        "c": BlocksMovement(passableForTags=["pass"])}
    tags_components = {"a": ["pass"]}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components)
    assert position_components["a"] == Position(x=0, y=0)
    assert position_components["b"] == Position(x=1, y=0)
