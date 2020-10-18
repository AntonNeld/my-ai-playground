from test_utils import room_from_yaml


def test_count_tags_score_additive():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    label: "player"
    score: 0
  d:
    tags:
      - "dirt"
  ".":
    countTagsScore:
      addTo: "player"
      scoreType: "additive"
      score: 1
      tags:
        dirt: 0
  a:
    - "d"
    - "."
room: |-
  p  a..
""")

    room.step()
    player = room.get_entities(label="player")[0]
    assert player.score == 2
    room.step()
    player = room.get_entities(label="player")[0]
    assert player.score == 4


def test_count_tags_score_constant():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    label: "player"
    score: 0
  d:
    tags:
      - "dirt"
  ".":
    countTagsScore:
      addTo: "player"
      scoreType: "constant"
      score: 1
      tags:
        dirt: 0
  a:
    - "d"
    - "."
room: |-
  p  a..
""")

    room.step()
    player_id, _ = room.get_entities(label="player", include_id=True)[0]
    assert room.get_entity_scores()[player_id] == 2
    room.step()
    player_id, _ = room.get_entities(label="player", include_id=True)[0]
    assert room.get_entity_scores()[player_id] == 2
