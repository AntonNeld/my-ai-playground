from pathlib import Path

import pytest

from dungeon.templating import (TemplateKeeper, template_from_txt,
                                Template, ParseError)

PARENT_DIR = Path(__file__).parent

RAW_TEMPLATE = Template(**{
    "entities": [
        {"position": {"x": 0, "y": 0}, "ai": {"kind": "pathfinder"},
         "looksLike": "player", "pickupper": {},
         "scoring": {"kind": "heldItems"}},
        {"position": {"x": 1, "y": 1}, "blocksMovement": True,
         "looksLike": "wall"},
        {"position": {"x": 1, "y": 0},
         "pickup": {"kind": "item"},
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
    template = template_from_txt("""
{
  "definitions": {
    "p": {
      "looksLike": "player",
      "pickupper": {},
      "ai": {"kind": "pathfinder"},
      "scoring": {"kind": "heldItems"}
    },
    "c": {"looksLike": "coin", "pickup": {"kind": "item"}},
    "#": {"looksLike": "wall", "blocksMovement": true}
  }
}

 #
pc

""")
    assert equal_templates(template, Template(**{
        "entities": [
            {"position": {"x": 0, "y": 0}, "ai": {"kind": "pathfinder"},
             "looksLike": "player", "pickupper": {},
             "scoring": {"kind": "heldItems"}},
            {"position": {"x": 1, "y": 1}, "blocksMovement": True,
             "looksLike": "wall"},
            {"position": {"x": 1, "y": 0},
             "pickup": {"kind": "item"},
             "looksLike": "coin"}
        ]
    }))


def test_parse_ignore_comment():
    template = template_from_txt("""
// This is a comment
{
  "definitions": {
    // This is a comment inside the JSON
    "p": {"looksLike": "player"}
  }
}

p

""")
    assert equal_templates(template, Template(**{
        "entities": [{"position": {"x": 0, "y": 0}, "looksLike": "player"}]
    }))


def test_parse_colocated_entities():
    template = template_from_txt("""
{
  "definitions": {
    "a": [{"looksLike": "player"}, {"looksLike": "wall"}]
  }
}

a

""")
    assert equal_templates(template, Template(**{
        "entities": [
            {"position": {"x": 0, "y": 0}, "looksLike": "player"},
            {"position": {"x": 0, "y": 0}, "looksLike": "wall"},
        ]
    }))


def test_parse_colocated_entities_with_refs():
    template = template_from_txt("""
{
  "definitions": {
    "a": [{"looksLike": "player"}, "#"],
    "#": {"looksLike": "wall"}
  }
}

a

""")
    assert equal_templates(template, Template(**{
        "entities": [
            {"position": {"x": 0, "y": 0}, "looksLike": "player"},
            {"position": {"x": 0, "y": 0}, "looksLike": "wall"},
        ]
    }))


def test_parse_nested_refs():
    template = template_from_txt("""
{
  "definitions": {
    "a": ["b"],
    "b": "c",
    "c": {"looksLike": "coin"}
  }
}

a

""")
    assert equal_templates(template, Template(**{
        "entities": [
            {"position": {"x": 0, "y": 0}, "looksLike": "coin"},
        ]
    }))


def test_parse_circular_refs():
    with pytest.raises(ParseError):
        template_from_txt("""
{
  "definitions": {
    "a": "b",
    "b": "c",
    "c": "a"
  }
}

a

""")


def test_included_templates_validate():
    template_keeper = TemplateKeeper()
    root_dir = Path(__file__).parent.parent.parent
    template_keeper.load_directory(
        root_dir / "server" / "dungeon" / "templates")


def test_template_not_modified_by_room():
    template = Template(**{
        "entities": [
            {"position": {"x": 0, "y": 0}, "looksLike": "player"},
        ]
    })
    room = template.create_room()
    room.get_entities()[0].position.x = 1
    assert template.entities[0].position.x == 0
