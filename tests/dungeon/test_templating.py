from pathlib import Path

import pytest

from dungeon.templating import (TemplateKeeper, template_from_txt,
                                Template, ParseError)
from dungeon.entity import Entity

PARENT_DIR = Path(__file__).parent

RAW_TEMPLATE = Template(**{
    "templateType": "raw",
    "entities": [
        {"position": {"x": 0, "y": 0}, "looksLike": "player"},
        {"position": {"x": 1, "y": 1}, "looksLike": "wall"},
        {"position": {"x": 1, "y": 0}, "looksLike": "coin"}
    ]
})

PARSED_TEXT_TEMPLATE = Template(**{
    "templateType": "raw",
    "entities": [
        {"position": {"x": 1, "y": 1}, "looksLike": "wall"},
        {"position": {"x": 0, "y": 0}, "looksLike": "player"},
        {"position": {"x": 1, "y": 0}, "looksLike": "coin"}
    ]
})


@pytest.fixture
def loaded_keeper():
    template_keeper = TemplateKeeper()
    template_keeper.load_directory(
        PARENT_DIR / "test_templating" / "templates")
    return template_keeper


def test_load_json(loaded_keeper):
    template = loaded_keeper.get_template("json_example")
    assert template == RAW_TEMPLATE


def test_load_yaml(loaded_keeper):
    template = loaded_keeper.get_template("yaml_example")
    assert template == RAW_TEMPLATE


def test_load_txt(loaded_keeper):
    template = loaded_keeper.get_template("txt_example")
    # This relies on the order of entities, but it is
    # temporary anyway.
    assert template == PARSED_TEXT_TEMPLATE


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
    assert template.create_room().get_entities() == [
        Entity(**{"looksLike": "player", "position": {"x": 0, "y": 0}})]


def test_parse_colocated_entities():
    template = template_from_txt("""
{
  "definitions": {
    "a": [{"looksLike": "player"}, {"looksLike": "wall"}]
  }
}

a

""")
    entities = template.create_room().get_entities()
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "player"}) in entities
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "wall"}) in entities


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
    entities = template.create_room().get_entities()
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "player"}) in entities
    assert Entity(**{"position": {"x": 0, "y": 0},
                     "looksLike": "wall"}) in entities


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
    assert template.create_room().get_entities() == [
        Entity(**{"looksLike": "coin", "position": {"x": 0, "y": 0}})]


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


def test_template_not_modified_by_room():
    template = Template(
        **{"templateType": "raw",
           "entities": [
               {"position": {"x": 0, "y": 0}, "looksLike": "player"},
           ]
           })
    room = template.create_room()
    room.get_entities()[0].position.x = 1
    assert template.entities[0].position.x == 0
