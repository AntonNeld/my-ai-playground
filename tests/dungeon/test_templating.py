from pathlib import Path

from dungeon.templating import TemplateKeeper

PARENT_DIR = Path(__file__).parent

RAW_TEMPLATE = {
    "entities": [
        {"x": 0, "y": 0, "type": "player", "ai": "pathfinder"},
        {"x": 1, "y": 1, "type": "block"},
        {"x": 1, "y": 0, "type": "coin"}
    ]
}


def test_load_json():
    template_keeper = TemplateKeeper()
    template_keeper.load_directory(PARENT_DIR / "templates")

    template = template_keeper.get_template("json_example")
    assert template == RAW_TEMPLATE
