import pytest
import random

from dungeon.systems import MovementSystem
from dungeon.consts import Move, Position
from dungeon.custom_component_dicts import PositionDict
from dungeon.entity import BlocksMovement


@pytest.mark.parametrize("direction,x,y",
                         [("up", 0, 1), ("down", 0, -1),
                          ("left", -1, 0), ("right", 1, 0)])
def test_move_direction(direction, x, y):
    system = MovementSystem()
    random_generator = random.Random(123)
    actions = {"a": Move(direction=direction)}
    position_components = PositionDict({"a": Position(x=0, y=0)})
    blocks_movement_components = {}
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components,
                         random_generator)
    assert position_components["a"] == Position(x=x, y=y)


def test_blocks_movement():
    system = MovementSystem()
    random_generator = random.Random(123)
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {"b": BlocksMovement()}
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components,
                         random_generator)
    assert position_components["a"] == Position(x=0, y=0)


def test_blocks_movement_wrong_tags():
    system = MovementSystem()
    random_generator = random.Random(123)
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {
        "b": BlocksMovement(passableForTags=["pass"])}
    tags_components = {"a": ["notPass"]}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components,
                         random_generator)
    assert position_components["a"] == Position(x=0, y=0)


def test_blocks_movement_right_tags():
    system = MovementSystem()
    random_generator = random.Random(123)
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {
        "b": BlocksMovement(passableForTags=["pass"])}
    tags_components = {"a": ["pass"]}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components,
                         random_generator)
    assert position_components["a"] == Position(x=1, y=0)


def test_blocker_cannot_move_into_others_space():
    system = MovementSystem()
    random_generator = random.Random(123)
    actions = {"a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {"a": BlocksMovement()}
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components,
                         random_generator)
    assert position_components["a"] == Position(x=0, y=0)


def test_movement_is_blocked_even_if_blocker_moves_away():
    system = MovementSystem()
    random_generator = random.Random(123)
    actions = {"b": Move(direction="up"), "a": Move(direction="right")}
    position_components = PositionDict(
        {"a": Position(x=0, y=0), "b": Position(x=1, y=0)})
    blocks_movement_components = {"b": BlocksMovement()}
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components,
                         random_generator)
    assert position_components["a"] == Position(x=0, y=0)


class MockRandom:

    def __init__(self, chosen):
        self.chosen = chosen

    def choice(self, iterable):
        return self.chosen


@pytest.mark.parametrize("chosen", ["a", "b", "c"])
def test_many_moving_into_same_space_winner_selected_randomly(chosen):
    system = MovementSystem()
    random_generator = MockRandom(chosen)
    actions = {"a": Move(direction="right"), "b": Move(
        direction="left"), "c": Move(direction="down")}
    position_components = PositionDict({
        "a": Position(x=0, y=0),
        "b": Position(x=2, y=0),
        "c": Position(x=1, y=1)
    })
    blocks_movement_components = {
        "a": BlocksMovement(),
        "b": BlocksMovement(),
        "c": BlocksMovement()
    }
    tags_components = {}
    system.move_entities(actions, position_components,
                         blocks_movement_components, tags_components,
                         random_generator)
    assert position_components[chosen] == Position(x=1, y=0)
    for entity_id in ("a", "b", "c"):
        if entity_id != chosen:
            assert position_components[entity_id] != Position(x=1, y=0)
