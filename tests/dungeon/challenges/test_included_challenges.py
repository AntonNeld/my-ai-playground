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
            "standard:vacuum": 198,
            "withMoveCost:vacuum": 197,
            "withMoveCostBetterSensors:vacuum": 197,
            "unknown1Random:vacuum": 788,
            "unknown2Random:vacuum": 783,
            "unknown3Random:vacuum": 804,
            "unknownPoorRandom:vacuum": 600,
            "unknown1Exploring:vacuum": 857,
            "unknown2Exploring:vacuum": 860,
            "unknown3Exploring:vacuum": 864,
            "unknownPoorExploring:vacuum": 858,
        }
    },
    {
        "challenge": "compare_search",
        "duration": 100,
        "scores": {
            "aStarGraph:player": 647,
            "aStarTree:player": 0,
            "breadthFirstGraph:player": 379,
            "breadthFirstTree:player": 0,
            "depthFirstGraph:player": 353,
            "depthFirstTree:player": 0,
            "depthFirstTreeCheckPath:player": 115,
            "depthLimitedGraph:player": 479,
            "depthLimitedTree:player": 0,
            "depthLimitedTreeCheckPath:player": 373,
            "greedyBestFirstGraph:player": 479,
            "greedyBestFirstTree:player": 0,
            "iterativeDeepeningGraph:player": 479,
            "iterativeDeepeningTree:player": 0,
            "iterativeDeepeningTreeCheckPath:player": 479,
            "uniformCostGraph:player": 647,
            "uniformCostTree:player": 0
        }
    },
    {
        "challenge": "compare_optimal_search",
        "duration": 50,
        "scores": {
            "aStarGraph:player": 951,
            "uniformCostGraph:player": 951
        }
    },
    {
        "challenge": "missionaries_and_cannibals",
        "duration": 110,
        "scores": {
            "boat": 5893,
        }
    }
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
