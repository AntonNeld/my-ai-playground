from dungeon.room import Room
from dungeon.entity import Entity, CountTagsScore
from dungeon.consts import Position


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
