import pytest

from dungeon.room import Room


@pytest.mark.parametrize("move,x,y",
                         [("move_up", 0, 1), ("move_down", 0, -1),
                          ("move_left", -1, 0), ("move_right", 1, 0)])
def test_action_move(move, x, y):
    room = Room(steps=0, entities={"a": {
        "x": 0,
        "y": 0,
        "looks_like": "player",
        "ai": {"kind": "singular", "move": move}
    }})
    room.step()
    assert room.get_entity("a").x == x
    assert room.get_entity("a").y == y
