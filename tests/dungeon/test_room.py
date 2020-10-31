from dungeon.room import Room
from dungeon.entity import Entity
from dungeon.components import CountTagsScore
from dungeon.components import Position

BASE_RANDOM_ROOM = {
    "entities": {
        "random_mover": {
            "ai": {"kind": "random"},
            "actions": {"move": {}},
            "position": {"x": 0, "y": 0}
        },
        "collider_one": {
            "position": {"x": 10, "y": 0},
            "ai": {
                "kind": "singular",
                "action": {
                    "actionType": "move",
                    "direction": "right"
                }
            },
            "actions": {"move": {}}
        },
        "collider_two": {
            "position": {"x": 12, "y": 0},
            "ai": {
                "kind": "singular",
                "action": {
                    "actionType": "move",
                    "direction": "left"
                }
            },
            "actions": {"move": {}}
        },
    }
}


def test_get_entity_scores():
    room = Room(entities={
        "internal_score_only": Entity(score=10),
        "tags_score_only": Entity(label="labelB"),
        "all_score_types": Entity(label="labelC", score=5),
        "tag_counter_b": Entity(
            position=Position(x=0, y=0),
            countTagsScore=CountTagsScore(
                addTo="labelB",
                scoreType="constant",
                score=1,
                tags={}
            )
        ),
        "tag_counter_c": Entity(
            position=Position(x=0, y=0),
            countTagsScore=CountTagsScore(
                addTo="labelC",
                scoreType="constant",
                score=1,
                tags={}
            )
        ),
    })

    assert room.get_entity_scores() == {
        "internal_score_only": 10,
        "tags_score_only": 1,
        "all_score_types": 6
    }


def test_room_randomness_different_for_different_seeds():
    room_one = Room(randomSeed=123, **BASE_RANDOM_ROOM)
    room_two = Room(randomSeed=321, **BASE_RANDOM_ROOM)
    room_one.step()
    room_two.step()
    assert room_one != room_two


def test_room_randomness_same_for_same_seeds():
    room_one = Room(randomSeed=123, **BASE_RANDOM_ROOM)
    room_two = Room(randomSeed=123, **BASE_RANDOM_ROOM)
    room_one.step()
    room_two.step()
    assert room_one == room_two
