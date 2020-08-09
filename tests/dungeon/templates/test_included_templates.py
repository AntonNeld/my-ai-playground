from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app import create_app

TESTS = [
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
        "scores": {"player": 2}
    },
    {
        "template": "small_room",
        "duration": 3,
        "scores": {"player": 2}
    },
]


@pytest.fixture
def preloaded_client():
    root_dir = Path(__file__).parent.parent.parent.parent
    app = create_app(template_dir=root_dir /
                     "server" / "dungeon" / "templates")
    return TestClient(app)


@pytest.mark.parametrize("test", TESTS, ids=[t["template"] for t in TESTS])
def test_included_template(preloaded_client, test):
    scores = preloaded_client.post(
        "/api/evaluate", json={"template": test["template"],
                               "duration": test["duration"]}).json()
    assert scores == test["scores"]
