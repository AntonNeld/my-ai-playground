from dungeon.entity import Entity
from dungeon.template.visual import VisualTemplate


def test_template_not_modified_by_room():
    template = VisualTemplate(**{
        "templateType": "visual",
        "definitions": {
            "p": {"looksLike": "player"},
        },
        "room": "p"
    })
    room = template.create_room()
    room.get_entities()[0].looks_like = "coin"
    assert template.definitions["p"].looks_like == "player"


def test_parse_colocated_entities():
    template = VisualTemplate(**{
        "templateType": "visual",
        "definitions": {
            "a": [{"looksLike": "player"}, {"looksLike": "wall"}]
        },
        "room": "a"
    })
    entities = template.create_room().get_entities()
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "player"}) in entities
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "wall"}) in entities
