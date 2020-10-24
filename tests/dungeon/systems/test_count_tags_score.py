from dungeon.systems import CountTagsScoreSystem
from dungeon.custom_component_dicts import PositionDict, LabelDict
from dungeon.consts import Position
from dungeon.entity import CountTagsScore


def test_right_amount_of_tags():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter": CountTagsScore(
            addTo="player",
            scoreType="constant",
            score=1,
            tags={
                "tagOne": 1,
                "tagTwo": 2
            }
        )
    }
    position_components = PositionDict({
        "counter": Position(x=0, y=0),
        "tag_holder": Position(x=0, y=0)
    })
    tags_components = {"tag_holder": ["tagOne", "tagTwo", "tagTwo"]}
    label_components = LabelDict({"p": "player"})
    scores = system.get_constant_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components
    )
    assert scores == {"p": 1}


def test_include_own_tags():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter": CountTagsScore(
            addTo="player",
            scoreType="constant",
            score=1,
            tags={
                "tagOne": 1,
                "tagTwo": 2
            }
        )
    }
    position_components = PositionDict({
        "counter": Position(x=0, y=0)
    })
    tags_components = {"counter": ["tagOne", "tagTwo", "tagTwo"]}
    label_components = LabelDict({"p": "player"})
    scores = system.get_constant_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components
    )
    assert scores == {"p": 1}


def test_combine_tags_from_different_entities():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter": CountTagsScore(
            addTo="player",
            scoreType="constant",
            score=1,
            tags={
                "tagOne": 1,
                "tagTwo": 2
            }
        )
    }
    position_components = PositionDict({
        "counter": Position(x=0, y=0),
        "tag_holder": Position(x=0, y=0)
    })
    tags_components = {"counter": ["tagOne"],
                       "tag_holder": ["tagTwo", "tagTwo"]}
    label_components = LabelDict({"p": "player"})
    scores = system.get_constant_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components
    )
    assert scores == {"p": 1}


def test_ignore_irrelevant_tags():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter": CountTagsScore(
            addTo="player",
            scoreType="constant",
            score=1,
            tags={
                "tagOne": 1,
                "tagTwo": 2
            }
        )
    }
    position_components = PositionDict({
        "counter": Position(x=0, y=0),
        "tag_holder": Position(x=0, y=0)
    })
    tags_components = {"tag_holder": [
        "tagOne", "tagTwo", "tagTwo", "tagThree"]}
    label_components = LabelDict({"p": "player"})
    scores = system.get_constant_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components
    )
    assert scores == {"p": 1}


def test_no_tags_always_give_score():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter": CountTagsScore(
            addTo="player",
            scoreType="constant",
            score=1,
            tags={}
        )
    }
    position_components = PositionDict({
        "counter": Position(x=0, y=0)
    })
    tags_components = {}
    label_components = LabelDict({"p": "player"})
    scores = system.get_constant_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components
    )
    assert scores == {"p": 1}


def test_multiple_counters_add_score():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter_one": CountTagsScore(
            addTo="player",
            scoreType="constant",
            score=1,
            tags={}
        ),
        "counter_two": CountTagsScore(
            addTo="player",
            scoreType="constant",
            score=1,
            tags={}
        ),
    }
    position_components = PositionDict({
        "counter_one": Position(x=0, y=0),
        "counter_two": Position(x=1, y=0)
    })
    tags_components = {}
    label_components = LabelDict({"p": "player"})
    scores = system.get_constant_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components
    )
    assert scores == {"p": 2}


def test_too_few_tags():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter": CountTagsScore(
            addTo="player",
            scoreType="constant",
            score=1,
            tags={
                "tagOne": 1,
                "tagTwo": 2
            }
        )
    }
    position_components = PositionDict({
        "counter": Position(x=0, y=0),
        "tag_holder": Position(x=0, y=0)
    })
    tags_components = {"tag_holder": ["tagOne", "tagTwo"]}
    label_components = LabelDict({"p": "player"})
    scores = system.get_constant_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components
    )
    assert scores == {}


def test_too_many_tags():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter": CountTagsScore(
            addTo="player",
            scoreType="constant",
            score=1,
            tags={
                "tagOne": 1,
                "tagTwo": 2
            }
        )
    }
    position_components = PositionDict({
        "counter": Position(x=0, y=0),
        "tag_holder": Position(x=0, y=0)
    })
    tags_components = {"tag_holder": ["tagOne", "tagTwo", "tagTwo", "tagTwo"]}
    label_components = LabelDict({"p": "player"})
    scores = system.get_constant_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components
    )
    assert scores == {}


def test_additive_score_type_adds_to_score():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter": CountTagsScore(
            addTo="player",
            scoreType="additive",
            score=1,
            tags={}
        )
    }
    position_components = PositionDict({
        "counter": Position(x=0, y=0)
    })
    tags_components = {}
    label_components = LabelDict({"p": "player"})
    score_components = {"p": 1}
    system.add_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components, score_components
    )
    assert score_components == {"p": 2}


def test_additive_score_type_no_effect_if_no_score():
    system = CountTagsScoreSystem()
    count_tags_score_components = {
        "counter": CountTagsScore(
            addTo="player",
            scoreType="additive",
            score=1,
            tags={}
        )
    }
    position_components = PositionDict({
        "counter": Position(x=0, y=0)
    })
    tags_components = {}
    label_components = LabelDict({"p": "player"})
    score_components = {}
    system.add_tag_scores(
        count_tags_score_components, position_components, tags_components,
        label_components, score_components
    )
    assert score_components == {}
