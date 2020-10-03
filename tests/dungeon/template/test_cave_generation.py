import pytest

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
    assert template.create_room().get_entities()


def test_correct_width(template):
    room = template.create_room()
    min_x = min([e.position.x for e in room.get_entities()])
    max_x = max([e.position.x for e in room.get_entities()])
    assert max_x + 1 - min_x == template.width


def test_correct_height(template):
    room = template.create_room()
    min_y = min([e.position.y for e in room.get_entities()])
    max_y = max([e.position.y for e in room.get_entities()])
    assert max_y + 1 - min_y == template.height


def test_no_overlap(template):
    room = template.create_room()
    for e in room.get_entities():
        assert len(room.get_entities_at(e.position.x, e.position.y)) == 1


def test_correct_amount_of_stuff(template):
    room = template.create_room()
    assert len(room.get_entities(looks_like="player")
               ) == template.stuff["p"].amount
    assert len(room.get_entities(looks_like="coin")
               ) == template.stuff["c"].amount


def test_template_not_modified_by_room(template):
    room = template.create_room()
    wall_entity = room.get_entities(looks_like="wall")[0]
    wall_entity.looks_like = "coin"
    player_entity = room.get_entities(looks_like="player")[0]
    player_entity.looks_like = "coin"
    assert template.definitions["#"].looks_like == "wall"
    assert template.definitions["p"].looks_like == "player"


def test_same_room_for_same_seed(template):
    room_one = template.create_room()
    room_two = template.create_room()
    assert sorted(room_one.get_entities(), key=lambda e: e.json()) == sorted(
        room_two.get_entities(), key=lambda e: e.json())


def test_different_rooms_for_different_seeds(template):
    room_one = template.create_room()
    template.seed = 234
    room_two = template.create_room()
    assert sorted(room_one.get_entities(), key=lambda e: e.json()) != sorted(
        room_two.get_entities(), key=lambda e: e.json())


def test_outside_is_not_connected_with_inside(template):
    room = template.create_room()
    # Let's designate the area with the player as "inside".
    # "Fill" the area and check that we never reach a location
    # with too large/small x or y.
    player = room.get_entities(looks_like="player")[0]
    edge = [(player.position.x, player.position.y)]
    filled = set()
    while edge:
        (x, y) = edge.pop()
        assert x >= 0
        assert x < template.width
        assert y >= 0
        assert y < template.height
        filled.add((x, y))
        for location in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if (location not in filled
                    and not [e for e in room.get_entities_at(
                        location[0], location[1]
                    ) if e.looks_like == "wall"]):
                edge.append(location)
