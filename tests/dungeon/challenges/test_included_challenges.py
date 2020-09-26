from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app import create_app

TESTS = [
    {
        "challenge": "maze",
        "duration": 13,
        "scores": {
            "standard:player": 3,
            "actionPickup:player": 2,
            "nearsighted:player": 1,
            "competition:playerOne": 2,
            "competition:playerTwo": 2
        }
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
    {
        "challenge": "vacuum_cleaner_world_unknown_1_randomized",
        "duration": 100,
        "scores": {"vacuum": 794}
    },
    {
        "challenge": "vacuum_cleaner_world_unknown_2_randomized",
        "duration": 100,
        "scores": {"vacuum": 802}
    },
    {
        "challenge": "vacuum_cleaner_world_unknown_3_randomized",
        "duration": 100,
        "scores": {"vacuum": 853}
    },
    {
        "challenge": "vacuum_cleaner_world_unknown_poor_randomized",
        "duration": 100,
        "scores": {"vacuum": 600}
    },
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
