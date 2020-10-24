import pytest
import json

from dungeon.template.cave_generation import CaveGenerationTemplate


@pytest.fixture
def template():
    return CaveGenerationTemplate(**{
        "templateType": "caveGeneration",
        "definitions": {
            "#": {"looksLike": "wall", "blocksMovement": {}},
            "p": {"looksLike": "player"},
            "c": {"looksLike": "coin"},
        },
        "seed": 123,
        "width": 10,
        "height": 5,
        "wall": "#",
        "stuff": {
            "p": {"amount": 1},
            "c": {"amount": 4},
        }
    })


def test_creates_a_room_with_entities(template):
    assert template.create_room().dict()["entities"]


def test_correct_width(template):
    room = template.create_room().dict()
    print(room)
    min_x = min([e["position"]["x"] for e in room["entities"].values()])
    max_x = max([e["position"]["x"] for e in room["entities"].values()])
    assert max_x + 1 - min_x == template.width


def test_correct_height(template):
    room = template.create_room().dict()
    min_y = min([e["position"]["y"] for e in room["entities"].values()])
    max_y = max([e["position"]["y"] for e in room["entities"].values()])
    assert max_y + 1 - min_y == template.height


def test_no_overlap(template):
    room = template.create_room().dict()
    positions = [(e["position"]["x"], e["position"]["y"])
                 for e in room["entities"].values()]
    assert len(positions) == len(set(positions))


def test_correct_amount_of_stuff(template):
    room = template.create_room().dict()
    looks_like = [e["looks_like"] for e in room["entities"].values()]
    assert looks_like.count("player") == template.stuff["p"].amount
    assert looks_like.count("coin") == template.stuff["c"].amount


def test_template_not_modified_by_room(template):
    room = template.create_room()
    for entity_id in room.list_entities():
        entity = room.get_entity(entity_id)
        entity.looks_like = "coin"
    assert template.definitions["#"].looks_like == "wall"
    assert template.definitions["p"].looks_like == "player"


def test_same_room_for_same_seed(template):
    room_one = template.create_room().dict()
    room_two = template.create_room().dict()
    assert (
        sorted(room_one["entities"].values(), key=lambda e: json.dumps(e))
        == sorted(room_two["entities"].values(), key=lambda e: json.dumps(e))
    )


def test_different_rooms_for_different_seeds(template):
    room_one = template.create_room().dict()
    template.seed = 234
    room_two = template.create_room().dict()
    assert (
        sorted(room_one["entities"].values(), key=lambda e: json.dumps(e))
        != sorted(room_two["entities"].values(), key=lambda e: json.dumps(e))
    )


def test_outside_is_not_connected_with_inside(template):
    room = template.create_room().dict()
    # Let's designate the area with the player as "inside".
    # "Fill" the area and check that we never reach a location
    # with too large/small x or y.
    player = [e for e in room["entities"].values()
              if e["looks_like"] == "player"][0]
    wall_locations = [(e["position"]["x"], e["position"]["y"])
                      for e in room["entities"].values()
                      if e["looks_like"] == "wall"]
    edge = [(player["position"]["x"], player["position"]["y"])]

    filled = set()
    while edge:
        (x, y) = edge.pop()
        assert x >= 0
        assert x < template.width
        assert y >= 0
        assert y < template.height
        filled.add((x, y))
        for location in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if location not in filled and location not in wall_locations:
                edge.append(location)
