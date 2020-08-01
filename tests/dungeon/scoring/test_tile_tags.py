from test_utils import room_from_text


def test_tile_tags():
    room = room_from_text("""
{
  "definitions": {
    "p": {
      "looksLike": "player",
      "scoring": {
        "kind": "tileTags",
        "shouldHaveTags": ["goodTag"],
        "shouldNotHaveTags": ["badTag"]
      }
    },
    "a": {"tags": ["goodTag"]},
    "b": {"tags": ["badTag"]},
    "c": {"tags": ["goodTag", "badTag"]}
  }
}

p a
 bc

    """)
    entity = room.get_entities(looks_like="player")[0]
    assert entity.scoring.get_score(entity, room) == 1


def test_no_double_counting():
    room = room_from_text("""
{
  "definitions": {
    "a": [
      {
        "looksLike": "player",
        "scoring": {
          "kind": "tileTags",
          "shouldHaveTags": ["goodTag"]
        }
      },
      {"tags": ["goodTag"]}
    ]
  }
}

a

    """)
    entity = room.get_entities(looks_like="player")[0]
    assert entity.scoring.get_score(entity, room) == 1
