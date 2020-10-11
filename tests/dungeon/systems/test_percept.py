from test_utils import room_from_yaml


def test_get_view():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    perception: {}
  c:
    looksLike: "coin"
  "#":
    looksLike: "wall"
room: |-2
     #
  p  c
""")

    perceptor_id, _ = room.get_entities(
        include_id=True, looks_like="player")[0]
    entities = room.percept_system.get_percepts(
        room.perception, room.position, room.looks_like, room.pickupper
    )[perceptor_id]["entities"]
    assert len(entities) == 2
    assert {"x": 3, "y": 0, "looks_like": "coin"} in entities
    assert {"x": 3, "y": 1, "looks_like": "wall"} in entities


def test_get_view_with_max_distance():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    perception:
      distance: 3
  c:
    looksLike: "coin"
  "#":
    looksLike: "wall"
room: |-
  #     #
     p  c
  #     #
""")

    perceptor_id, _ = room.get_entities(
        include_id=True, looks_like="player")[0]
    entities = room.percept_system.get_percepts(
        room.perception, room.position, room.looks_like, room.pickupper
    )[perceptor_id]["entities"]
    assert len(entities) == 1
    assert {"x": 3, "y": 0, "looks_like": "coin"} in entities


def test_get_view_with_position():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    perception:
      includePosition: true
  "#":
    looksLike: "wall"
room: |-2
     #
  # p
""")

    perceptor_id, _ = room.get_entities(
        include_id=True, looks_like="player")[0]
    position = room.percept_system.get_percepts(
        room.perception, room.position, room.looks_like, room.pickupper
    )[perceptor_id]["position"]
    assert position["x"] == 2
    assert position["y"] == 0


def test_get_view_inventory():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    perception: {}
    pickupper:
      inventory:
        - looksLike: "coin"
        - looksLike: "evilCoin"
room: |-
  p
""")
    perceptor_id, _ = room.get_entities(
        include_id=True, looks_like="player")[0]
    assert room.percept_system.get_percepts(
        room.perception, room.position, room.looks_like, room.pickupper
    )[perceptor_id]["inventory"] == ["coin", "evilCoin"]
