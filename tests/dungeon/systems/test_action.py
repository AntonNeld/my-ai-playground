import random
from unittest import mock

from dungeon.systems import ActionSystem
from dungeon.consts import Move, DoNothing
from dungeon.entity import ActionDetails
from dungeon.custom_component_dicts import LabelDict
from profiling import time_profiling, memory_profiling


class MockAI:

    def __init__(self, action):
        self.action = action

    def next_action(self, percept, random_generator):
        return self.action


def test_get_action_from_ai():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai_components = {"a": MockAI(Move(direction="right"))}
    percepts = {}
    actions_components = {"a": {"move": ActionDetails()}}
    score_components = {}
    label_components = LabelDict({})
    actions = system.get_actions(ai_components, percepts, actions_components,
                                 score_components, label_components,
                                 random_generator)
    assert actions == {"a": Move(direction="right")}


def test_do_not_include_do_nothing():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai_components = {"a": MockAI(DoNothing())}
    percepts = {}
    actions_components = {"a": {"none": ActionDetails()}}
    score_components = {}
    label_components = LabelDict({})
    actions = system.get_actions(ai_components, percepts, actions_components,
                                 score_components, label_components,
                                 random_generator)
    assert actions == {}


def test_only_include_allowed_actions():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai_components = {"a": MockAI(Move(direction="right"))}
    percepts = {}
    actions_components = {}
    score_components = {}
    label_components = LabelDict({})
    actions = system.get_actions(ai_components, percepts, actions_components,
                                 score_components, label_components,
                                 random_generator)
    assert actions == {}


def test_apply_action_penalty():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai_components = {"a": MockAI(Move(direction="right"))}
    percepts = {}
    actions_components = {"a": {"move": ActionDetails(cost=3)}}
    score_components = {"a": 0}
    label_components = LabelDict({})
    system.get_actions(ai_components, percepts, actions_components,
                       score_components, label_components, random_generator)
    assert score_components == {"a": -3}


def test_no_action_penalty_if_no_score_component():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai_components = {"a": MockAI(Move(direction="right"))}
    percepts = {}
    actions_components = {"a": {"move": ActionDetails(cost=3)}}
    score_components = {}
    label_components = LabelDict({})
    system.get_actions(ai_components, percepts, actions_components,
                       score_components, label_components, random_generator)
    assert score_components == {}


def test_do_profiling():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai_components = {"a": MockAI(DoNothing())}
    percepts = {}
    actions_components = {}
    score_components = {}
    label_components = LabelDict({"a": "player"})
    time_profiling.start()
    memory_profiling.start()
    system.get_actions(ai_components, percepts, actions_components,
                       score_components, label_components, random_generator)
    time_profiling.stop()
    memory_profiling.stop()
    assert "player" in time_profiling.get_result()["contexts"]
    assert "player" in memory_profiling.get_result()


def test_no_profiling_if_no_label():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai_components = {"a": MockAI(DoNothing())}
    percepts = {}
    actions_components = {}
    score_components = {}
    label_components = LabelDict({})
    time_profiling.start()
    memory_profiling.start()
    system.get_actions(ai_components, percepts, actions_components,
                       score_components, label_components, random_generator)
    time_profiling.stop()
    memory_profiling.stop()
    assert time_profiling.get_result()["contexts"] == {}
    assert memory_profiling.get_result() == {}


class FullMockAI:

    def __init__(self, action):
        self.action = action

    def update_state_percept(self, percept):
        pass

    def next_action(self, percept, random_generator):
        return self.action

    def update_state_action(self, action):
        pass


def test_call_update_state_percept():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai = FullMockAI(DoNothing())
    ai_components = {"a": ai}
    percepts = {"a": {"entities": []}}
    actions_components = {}
    score_components = {}
    label_components = LabelDict({})
    with mock.patch.object(ai, "update_state_percept") as update_state_percept:
        system.get_actions(
            ai_components, percepts, actions_components,
            score_components, label_components, random_generator)
        assert update_state_percept.call_args == mock.call({"entities": []})


def test_call_next_action_with_percept_and_generator():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai = FullMockAI(DoNothing())
    ai_components = {"a": ai}
    percepts = {"a": {"entities": []}}
    actions_components = {}
    score_components = {}
    label_components = LabelDict({})
    with mock.patch.object(
            ai, "next_action", wraps=ai.next_action) as next_action:
        system.get_actions(
            ai_components, percepts, actions_components,
            score_components, label_components, random_generator)
        assert next_action.call_args == mock.call(
            {"entities": []}, random_generator)


def test_no_percept_means_empty_dict():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai = FullMockAI(DoNothing())
    ai_components = {"a": ai}
    percepts = {}
    actions_components = {}
    score_components = {}
    label_components = LabelDict({})
    with mock.patch.object(ai, "update_state_percept") as update_state_percept:
        with mock.patch.object(
                ai, "next_action", wraps=ai.next_action) as next_action:
            system.get_actions(
                ai_components, percepts, actions_components,
                score_components, label_components, random_generator)
            assert update_state_percept.call_args == mock.call({})
            assert next_action.call_args == mock.call({}, random_generator)


def test_call_update_state_action():
    system = ActionSystem()
    random_generator = random.Random(123)
    ai = FullMockAI(Move(direction="right"))
    ai_components = {"a": ai}
    percepts = {}
    actions_components = {"a": {"move": ActionDetails()}}
    score_components = {}
    label_components = LabelDict({})
    with mock.patch.object(ai, "update_state_action") as update_state_action:
        system.get_actions(
            ai_components, percepts, actions_components,
            score_components, label_components, random_generator)
        assert update_state_action.call_args == mock.call(
            Move(action_type="move", direction="right")
        )
