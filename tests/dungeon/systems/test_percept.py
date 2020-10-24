from dungeon.systems import PerceptSystem
from dungeon.custom_component_dicts import PositionDict
from dungeon.entity import Perception, Pickupper, Entity
from dungeon.consts import Position


def test_percept_include_entities():
    system = PerceptSystem()
    perception_components = {"perceptor": Perception()}
    position_components = PositionDict(
        {"perceptor": Position(x=0, y=0), "otherEntity": Position(x=1, y=1)})
    looks_like_components = {"otherEntity": "coin"}
    pickupper_components = {}
    percepts = system.get_percepts(perception_components, position_components,
                                   looks_like_components, pickupper_components)
    assert percepts == {
        "perceptor": {
            "entities": [{"x": 1, "y": 1, "looks_like": "coin"}]
        }
    }


def test_percept_excludes_self():
    system = PerceptSystem()
    perception_components = {"perceptor": Perception()}
    position_components = PositionDict(
        {"perceptor": Position(x=0, y=0), "otherEntity": Position(x=1, y=1)})
    looks_like_components = {"otherEntity": "coin", "perceptor": "player"}
    pickupper_components = {}
    percepts = system.get_percepts(perception_components, position_components,
                                   looks_like_components, pickupper_components)
    assert percepts == {
        "perceptor": {
            "entities": [{"x": 1, "y": 1, "looks_like": "coin"}]
        }
    }


def test_percept_exclude_entities_beyond_max_distance():
    system = PerceptSystem()
    perception_components = {"perceptor": Perception(distance=3)}
    position_components = PositionDict({
        "perceptor": Position(x=0, y=0),
        "otherEntity": Position(x=3, y=0),
        "farEntityOne": Position(x=3, y=1),
        "farEntityTwo": Position(x=3, y=-1),
        "farEntityThree": Position(x=-3, y=1),
        "farEntityFour": Position(x=-3, y=-1),
    })
    looks_like_components = {
        "otherEntity": "coin",
        "farEntityOne": "wall",
        "farEntityTwo": "wall",
        "farEntityThree": "wall",
        "farEntityFour": "wall",
    }
    pickupper_components = {}
    percepts = system.get_percepts(perception_components, position_components,
                                   looks_like_components, pickupper_components)
    assert percepts == {
        "perceptor": {
            "entities": [{"x": 3, "y": 0, "looks_like": "coin"}]
        }
    }


def test_percept_include_position():
    system = PerceptSystem()
    perception_components = {"perceptor": Perception(includePosition=True)}
    position_components = PositionDict({"perceptor": Position(x=0, y=0)})
    looks_like_components = {}
    pickupper_components = {}
    percepts = system.get_percepts(perception_components, position_components,
                                   looks_like_components, pickupper_components)
    assert percepts == {
        "perceptor": {
            "entities": [],
            "position": {"x": 0, "y": 0}
        }
    }


def test_get_percept_include_inventory():
    system = PerceptSystem()
    perception_components = {"perceptor": Perception()}
    position_components = PositionDict({"perceptor": Position(x=0, y=0)})
    looks_like_components = {}
    pickupper_components = {
        "perceptor": Pickupper(
            inventory=[
                Entity(looksLike="coin"),
                Entity(looksLike="evilCoin")
            ]
        )
    }
    percepts = system.get_percepts(perception_components, position_components,
                                   looks_like_components, pickupper_components)
    assert percepts == {
        "perceptor": {
            "entities": [],
            "inventory": ["coin", "evilCoin"]
        }
    }
