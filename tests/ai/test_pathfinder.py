from test_utils import room_from_text


def test_find_coins_auto_pickup():
    room = room_from_text("""
{
  "definitions": {
    "p": {
      "looksLike": "player",
      "ai": {"kind": "pathfinder"},
      "canPickup": {},
      "perception": {}
    },
    "#": {"looksLike": "wall", "blocksMovement": true},
    "c": {"looksLike": "coin", "pickup": {"kind": "addScore", "score": 1}}
  }
}

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


def test_find_coins_action_pickup():
    room = room_from_text("""
{
  "definitions": {
    "p": {
      "looksLike": "player",
      "ai": {"kind": "pathfinder", "manualPickup": true},
      "canPickup": {"mode": "action"},
      "perception": {}
    },
    "#": {"looksLike": "wall", "blocksMovement": true},
    "c": {"looksLike": "coin", "pickup": {"kind": "addScore", "score": 1}}
  }
}

#########
#p#c#  c#
# # # ###
#   # #
###   #
  #####
    """)

    room.step(18)
    assert room.get_entities(looks_like="player")[0].score == 2
    assert room.get_entities(looks_like="coin") == []
