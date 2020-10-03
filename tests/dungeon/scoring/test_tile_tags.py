from test_utils import room_from_yaml


def test_tile_tags():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    scoring:
      kind: "tileTags"
      score: 10
      shouldHaveTags:
        - "goodTag"
      shouldNotHaveTags:
        - "badTag"
  a:
    tags:
      - "goodTag"
  b:
    tags:
      - "badTag"
  c:
    tags:
      - "goodTag"
      - "badTag"
room: |-
  p a
   bc
""")

    entity = room.get_entities(looks_like="player")[0]
    assert entity.scoring.get_score(entity, room) == 10


def test_no_double_counting():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  a:
    - looksLike: "player"
      scoring:
        kind: "tileTags"
        shouldHaveTags:
          - "goodTag"
    - tags:
      - "goodTag"
room: |-
  a
""")

    entity = room.get_entities(looks_like="player")[0]
    assert entity.scoring.get_score(entity, room) == 1
