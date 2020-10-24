import pytest

from dungeon.systems import AttackSystem
from dungeon.consts import Attack, Position
from dungeon.entity import Vulnerable
from dungeon.custom_component_dicts import PositionDict


@pytest.mark.parametrize(
    "direction,target_x,target_y",
    [("up", 0, 1), ("down", 0, -1), ("left", -1, 0), ("right", 1, 0)]
)
def test_attack_vulnerable(direction, target_x, target_y):
    actions = {"attacker": Attack(direction=direction)}
    position_components = PositionDict({
        "attacker": Position(x=0, y=0),
        "target": Position(x=target_x, y=target_y)
    })
    vulnerable_components = {"target": Vulnerable}
    system = AttackSystem()
    removed_entities = system.do_attacks(
        actions, position_components, vulnerable_components)
    assert "target" in removed_entities


def test_attack_empty_tile():
    actions = {"attacker": Attack(direction="right")}
    position_components = PositionDict({
        "attacker": Position(x=0, y=0)
    })
    vulnerable_components = {}
    system = AttackSystem()
    removed_entities = system.do_attacks(
        actions, position_components, vulnerable_components)
    assert len(removed_entities) == 0


def test_attack_invulnerable():
    actions = {"attacker": Attack(direction="right")}
    position_components = PositionDict({
        "attacker": Position(x=0, y=0),
        "target": Position(x=1, y=0)
    })
    vulnerable_components = {}
    system = AttackSystem()
    removed_entities = system.do_attacks(
        actions, position_components, vulnerable_components)
    assert len(removed_entities) == 0
