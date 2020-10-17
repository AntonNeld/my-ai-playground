from test_utils import room_from_yaml


def test_item_provides_tags():
    room = room_from_yaml("""
templateType: "visual"
definitions:
  p:
    looksLike: "player"
    ai:
      kind: "singular"
      action:
        actionType: "move"
        direction: "right"
    pickupper: {}
    actions:
      move: {}
    tags:
      - "tagZero"
  c:
    pickup:
      kind: "item"
      providesTags:
        - "tagOne"
        - "tagTwo"
room: |-
  pc
""")
    room.step()
    all_tags = room.tag_system.get_tags(
        room.tags_components, room.pickupper_components)
    entity_id, _ = room.get_entities(looks_like="player", include_id=True)[0]
    tags = all_tags[entity_id]
    assert "tagZero" in tags
    assert "tagOne" in tags
    assert "tagTwo" in tags
