from test_utils import room_from_text


def test_find_coins():
    room = room_from_text("""
p = {"looksLike": "player", "ai": {"kind": "pathfinder"}, "canPickup": true}
# = {"looksLike": "wall", "blocksMovement": true}
c = {"looksLike": "coin", "pickup": {"kind": "addScore", "score": 1}}

#########
#p#c#  c#
# # # ###
#   # #
###   #
  #####
    """)

    room.step(16)
    assert room.get_entities(looks_like="player")[0].score == 2
    assert room.get_entities(looks_like="coin") == []
