from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.actions import PickUp, DoNothing, Move
from .search import a_star_graph, NoSolutionError
from .problems.pathfinding import PathfindingProblem, get_heuristic


class GetNearestCoinAI(BaseModel):
    kind: Literal["getNearestCoin"]
    manual_pickup: bool = Field(False, alias="manualPickup")

    def next_action(self, percept, random_generator):
        if (self.manual_pickup and {"x": 0, "y": 0, "looks_like": "coin"}
                in percept["entities"]):
            return PickUp()

        walls = [(e["x"], e["y"]) for e in percept["entities"]
                 if e["looks_like"] == "wall"]
        coins = [(e["x"], e["y"]) for e in percept["entities"]
                 if e["looks_like"] == "coin"]
        if not coins:
            return DoNothing()
        problem = PathfindingProblem((0, 0), coins, walls, [])
        try:
            plan = a_star_graph(problem, get_heuristic(problem))
            return Move(direction=plan[0])
        except NoSolutionError:
            return DoNothing()
