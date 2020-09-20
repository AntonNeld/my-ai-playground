from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app import create_app

TESTS = [
    {
        "template": "competition",
        "duration": 15,
        "scores": {"playerOne": 2, "playerTwo": 2}
    },
    {
        "template": "maze",
        "duration": 13,
        "scores": {"player": 3}
    },
    {
        "template": "maze_action_pickup",
        "duration": 13,
        "scores": {"player": 2}
    },
    {
        "template": "maze_with_nearsighted_agent",
        "duration": 25,
        "scores": {"player": 1}
    },
    {
        "template": "singular_agent",
        "duration": 20,
        "scores": {"player": 2}
    },
    {
        "template": "small_room",
        "duration": 3,
        "scores": {"player": 2}
    },
    {
        "template": "vacuum_cleaner_world",
        "duration": 100,
        "scores": {"vacuum": 197}
    },
    {
        "template": "vacuum_cleaner_world_move_cost",
        "duration": 100,
        "scores": {"vacuum": 196}
    },
    {
        "template": "vacuum_cleaner_world_move_cost_better_sensors",
        "duration": 100,
        "scores": {"vacuum": 196}
    },
    # We can't include the randomized vacuum agents since tests should
    # be deterministic
    {
        "template": "vacuum_cleaner_world_unknown_1_exploring",
        "duration": 100,
        "scores": {"vacuum": 851}
    },
    {
        "template": "vacuum_cleaner_world_unknown_2_exploring",
        "duration": 100,
        "scores": {"vacuum": 870}
    },
    {
        "template": "vacuum_cleaner_world_unknown_3_exploring",
        "duration": 100,
        "scores": {"vacuum": 871}
    },
    {
        "template": "vacuum_cleaner_world_unknown_poor_exploring",
        "duration": 100,
        "scores": {"vacuum": 844}
    },
]

root_dir = Path(__file__).parent.parent.parent.parent
app = create_app(template_dir=root_dir /
                 "server" / "dungeon" / "templates")
test_client = TestClient(app)


@pytest.fixture
def preloaded_client():
    test_client.post("/state/clear")
    return test_client


@pytest.mark.parametrize("test", TESTS, ids=[t["template"] for t in TESTS])
def test_included_template(preloaded_client, test):
    result = preloaded_client.post(
        "/api/evaluate", json={"template": test["template"],
                               "duration": test["duration"]}).json()
    scores = result["scores"]
    assert scores == test["scores"]
