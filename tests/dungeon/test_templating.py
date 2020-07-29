from pathlib import Path

import pytest

from dungeon.templating import TemplateKeeper, template_from_txt, Template

PARENT_DIR = Path(__file__).parent

RAW_TEMPLATE = Template(**{
    "entities": [
        {"x": 0, "y": 0, "ai": {"kind": "pathfinder"},
         "looksLike": "player", "canPickup": True},
        {"x": 1, "y": 1, "blocksMovement": True,
         "looksLike": "wall"},
        {"x": 1, "y": 0, "pickup": {"kind": "addScore", "score": 1},
         "looksLike": "coin"}
    ]
})


def equal_templates(one, two):
    if ({key: value for key, value in one.dict().items()
         if key != "entities"} != {key: value for key, value in
                                   two.dict().items() if key != "entities"}):
        return False
    return (sorted(one.entities,
                   key=lambda x: x.json(sort_keys=True))
            == sorted(two.entities,
                      key=lambda x: x.json(sort_keys=True)))


@ pytest.fixture
def loaded_keeper():
    template_keeper = TemplateKeeper()
    template_keeper.load_directory(
        PARENT_DIR / "test_templating" / "templates")
    return template_keeper


def test_load_json(loaded_keeper):
    template = loaded_keeper.get_template("json_example")
    assert equal_templates(template, RAW_TEMPLATE)


def test_load_txt(loaded_keeper):
    template = loaded_keeper.get_template("txt_example")
    assert equal_templates(template, RAW_TEMPLATE)


def test_parse_txt():
    template = template_from_txt(
        """
p = player
c = coin
# = block

 #
pc

"""
    )
    assert equal_templates(template, Template(**{
        "entities": [
            {"x": 0, "y": 0, "ai": {"kind": "pathfinder"},
             "looksLike": "player", "canPickup": True},
            {"x": 1, "y": 1, "blocksMovement": True,
             "looksLike": "wall"},
            {"x": 1, "y": 0, "pickup": {"kind": "addScore", "score": 1},
             "looksLike": "coin"}
        ]
    }))


def test_included_templates_validate():
    template_keeper = TemplateKeeper()
    root_dir = Path(__file__).parent.parent.parent
    template_keeper.load_directory(
        root_dir / "server" / "dungeon" / "templates")


def test_template_not_modified_by_room():
    template_keeper = TemplateKeeper()
    template = Template(**{
        "entities": [
            {"x": 0, "y": 0, "looksLike": "player"},
        ]
    })
    template_keeper.add_template(template, template_id="testtemplate")
    room = template_keeper.create_room("testtemplate")
    room.get_entities()[0].x = 1
    assert template.entities[0].x == 0
