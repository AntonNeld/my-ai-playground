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
    assert room.get_entities()[0].position.x == x
    assert room.get_entities()[0].position.y == y


def test_blocks_movement():
    room = room_from_text("""
p = {"looksLike": "player", "ai": {"kind": "singular", "move": "move_right"}}
# = {"blocksMovement": true}

p#
    """)

    room.step()
    assert room.get_entities(looks_like="player")[0].position.x == 0


def test_score_pickup():
    room = room_from_text("""
p = {
      "looksLike": "player",
      "ai": {"kind": "singular", "move": "move_right"},
      "canPickup": "auto"
    }
c = {"pickup": {"kind": "addScore", "score": 1}}

pc
    """)

    room.step()
    assert len(room.get_entities()) == 1
    assert room.get_entities()[0].score == 1


def test_score_pickup_action():
    room = room_from_text("""
p = {
      "looksLike": "player",
      "ai": {"kind": "singular", "move": "move_right"},
      "canPickup": "action"
    }
c = {"pickup": {"kind": "addScore", "score": 1}}

pc
    """)

    room.step()
    assert len(room.get_entities()) == 2
    assert room.get_entities()[0].score is None
    room.get_entities(looks_like="player")[0].ai.move = "pick_up"
    room.step()
    assert len(room.get_entities()) == 1
    assert room.get_entities()[0].score == 1


def test_get_view():
    room = room_from_text("""
p = {"looksLike": "player", "perception": {}}
c = {"looksLike": "coin"}
# = {"looksLike": "wall"}

   #
p  c
    """)
    perceptor = room.get_entities(looks_like="player")[0]
    view = room.get_view(perceptor)
    assert len(view) == 2
    assert {"x": 3, "y": 0, "looks_like": "coin"} in view
    assert {"x": 3, "y": 1, "looks_like": "wall"} in view


def test_get_view_with_max_distance():
    room = room_from_text("""
p = {"looksLike": "player", "perception": {"distance": 3}}
c = {"looksLike": "coin"}
# = {"looksLike": "wall"}

#     #
   p  c
#     #
    """)
    perceptor = room.get_entities(looks_like="player")[0]
    view = room.get_view(perceptor)
    assert len(view) == 1
    assert {"x": 3, "y": 0, "looks_like": "coin"} in view
