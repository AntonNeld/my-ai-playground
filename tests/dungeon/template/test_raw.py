from dungeon.template.raw import RawTemplate


def test_template_not_modified_by_room():
    template = RawTemplate(**{
        "templateType": "raw",
        "entities": [
            {"position": {"x": 0, "y": 0}, "looksLike": "player"},
        ]
    })
    room = template.create_room()
    entity_id = room.list_entities()[0]
    room.get_entity(entity_id).position.x = 1
    assert template.entities[0].position.x == 0
