import json
from pathlib import Path

import pytest

from dungeon.templating import TemplateKeeper, template_from_txt

PARENT_DIR = Path(__file__).parent

RAW_TEMPLATE = {
    "entities": [
        {"x": 0, "y": 0, "type": "player", "ai": "pathfinder"},
        {"x": 1, "y": 1, "type": "block"},
        {"x": 1, "y": 0, "type": "coin"}
    ]
}


def equal_templates(one, two):
    if ({key: value for key, value in one.items() if key != "entities"} !=
            {key: value for key, value in two.items() if key != "entities"}):
        return False
    return (sorted(one["entities"],
                   key=lambda x: json.dumps(x, sort_keys=True))
            == sorted(two["entities"],
                      key=lambda x: json.dumps(x, sort_keys=True)))


@ pytest.fixture
def loaded_keeper():
    template_keeper = TemplateKeeper()
    template_keeper.load_directory(PARENT_DIR / "templates")
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
    assert equal_templates(template, {
        "entities": [
            {"x": 0, "y": 0, "type": "player", "ai": "pathfinder"},
            {"x": 1, "y": 1, "type": "block"},
            {"x": 1, "y": 0, "type": "coin"}
        ]
    })