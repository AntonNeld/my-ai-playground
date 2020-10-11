from test_utils import room_from_yaml


def test_count_tags_score():
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
