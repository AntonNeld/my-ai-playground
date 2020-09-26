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
        "scores": {
            "standard:vacuum": 197,
            "withMoveCost:vacuum": 196,
            "withMoveCostBetterSensors:vacuum": 196,
            "unknown1Random:vacuum": 794,
            "unknown2Random:vacuum": 802,
            "unknown3Random:vacuum": 853,
            "unknownPoorRandom:vacuum": 600,
            "unknown1Exploring:vacuum": 851,
            "unknown2Exploring:vacuum": 870,
            "unknown3Exploring:vacuum": 871,
            "unknownPoorExploring:vacuum": 844,
        }
    },
    {
        "challenge": "compare_search",
        "duration": 50,
        "scores": {
            "breadthFirstGraph:player": 871,
            "breadthFirstTree:player": 0,
            "uniformCostGraph:player": 957,
            "uniformCostTree:player": 0
        }
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
