import pytest

from test_utils import room_from_text


@pytest.mark.parametrize("move,x,y",
                         [("move_up", 0, 1), ("move_down", 0, -1),
                          ("move_left", -1, 0), ("move_right", 1, 0)])
def test_action_move(move, x, y):
    room = room_from_text(f"""
p = {{"ai": {{"kind": "singular", "move": "{move}"}}}}

p
    """)

    room.step()
    assert room.get_entities()[0].x == x
    assert room.get_entities()[0].y == y


def test_blocks_movement():
    room = room_from_text("""
p = {"looksLike": "player", "ai": {"kind": "singular", "move": "move_right"}}
# = {"blocksMovement": true}

p#
    """)

    room.step()
    assert room.get_entities(looks_like="player")[0].x == 0
