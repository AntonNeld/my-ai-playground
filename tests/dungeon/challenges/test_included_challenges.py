from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app import create_app

TESTS = [
    {
        "challenge": "competition",
        "duration": 15,
        "scores": {"playerOne": 2, "playerTwo": 2}
    },
    {
        "challenge": "maze",
        "duration": 13,
        "scores": {"player": 3}
    },
    {
        "challenge": "maze_action_pickup",
        "duration": 13,
        "scores": {"player": 2}
    },
    {
        "challenge": "maze_with_nearsighted_agent",
        "duration": 25,
        "scores": {"player": 1}
    },
    {
        "challenge": "singular_agent",
        "duration": 20,
        "scores": {"player": 2}
    },
    {
        "challenge": "small_room",
        "duration": 3,
        "scores": {"player": 2}
    },
    {
        "challenge": "vacuum_cleaner_world",
        "duration": 100,
        "scores": {"vacuum": 197}
    },
    {
        "challenge": "vacuum_cleaner_world_move_cost",
        "duration": 100,
        "scores": {"vacuum": 196}
    },
    {
        "challenge": "vacuum_cleaner_world_move_cost_better_sensors",
        "duration": 100,
        "scores": {"vacuum": 196}
    },
    # We can't include the randomized vacuum agents since tests should
    # be deterministic
    {
        "challenge": "vacuum_cleaner_world_unknown_1_exploring",
        "duration": 100,
        "scores": {"vacuum": 851}
    },
    {
        "challenge": "vacuum_cleaner_world_unknown_2_exploring",
        "duration": 100,
        "scores": {"vacuum": 870}
    },
    {
        "challenge": "vacuum_cleaner_world_unknown_3_exploring",
        "duration": 100,
        "scores": {"vacuum": 871}
    },
    {
        "challenge": "vacuum_cleaner_world_unknown_poor_exploring",
        "duration": 100,
        "scores": {"vacuum": 844}
    },
]

root_dir = Path(__file__).parent.parent.parent.parent
app = create_app(challenge_dir=root_dir /
                 "server" / "dungeon" / "challenges")
test_client = TestClient(app)


@pytest.fixture
def preloaded_client():
    test_client.post("/state/clear")
    return test_client


@pytest.mark.parametrize("test", TESTS, ids=[t["challenge"] for t in TESTS])
def test_included_challenge(preloaded_client, test):
    result = preloaded_client.post(
        "/api/evaluate", json={"challenge": test["challenge"],
                               "duration": test["duration"]}).json()
    scores = {key: value["score"] for key, value in result["entities"].items()}
    assert scores == test["scores"]
