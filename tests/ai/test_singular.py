from test_utils import room_from_text


def test_move_right():
    room = room_from_text("""
p = {"looksLike": "player", "ai": {"kind": "singular", "move": "move_right"}}

p
    """)

    assert room.get_entities(looks_like="player")[0].x == 0
    room.step()
    assert room.get_entities(looks_like="player")[0].x == 1
    room.step()
    assert room.get_entities(looks_like="player")[0].x == 2
