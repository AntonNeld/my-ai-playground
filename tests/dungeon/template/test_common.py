import pytest

from dungeon.template.common import translate_definition_symbol, ParseError
from dungeon.entity import Entity


def test_parse_nested_refs():
    definitions = {
        "a": ["b"],
        "b": "c",
        "c": Entity(**{"looksLike": "coin"})
    }
    assert translate_definition_symbol("a", definitions) == [
        Entity(**{"looksLike": "coin"})
    ]


def test_parse_circular_refs():
    definitions = {
        "a": "b",
        "b": "c",
        "c": "a"
    }
    with pytest.raises(ParseError):
        translate_definition_symbol("a", definitions)
