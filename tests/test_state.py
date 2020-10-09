from pathlib import Path

import pytest

from dungeon.challenge_keeper import Challenge
from state import StateKeeper

PARENT_DIR = Path(__file__).parent

RAW_CHALLENGE = Challenge(**{
    "template": {
        "templateType": "raw",
        "entities": [
            {"position": {"x": 0, "y": 0}, "looksLike": "player"},
            {"position": {"x": 1, "y": 1}, "looksLike": "wall"},
            {"position": {"x": 1, "y": 0}, "looksLike": "coin"}
        ]
    }
})


@pytest.fixture
def loaded_state():
    state_keeper = StateKeeper(PARENT_DIR / "test_state" / "challenges")
    state_keeper.load_challenge_directory()
    return state_keeper


def test_load_json(loaded_state):
    challenge = loaded_state.challenge_keeper.get_challenge("json_example")
    assert challenge == RAW_CHALLENGE


def test_load_yaml(loaded_state):
    challenge = loaded_state.challenge_keeper.get_challenge("yaml_example")
    assert challenge == RAW_CHALLENGE
