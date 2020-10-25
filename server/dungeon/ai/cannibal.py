from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import DoNothing, Move, Attack
from .search import a_star_graph, NoSolutionError
from .problems.pathfinding import PathfindingProblem, get_heuristic


class CannibalAI(BaseModel):
    # Cannibal from exercise 3.9
    # If it can reach more cannibals (including itself) than missionaries
    # it will attack the nearest missionary (unless the player is also there)
    kind: Literal["cannibal"]

    def next_action(self, percept, random_generator):
        if "position" not in percept:
            # We are picked up
            return DoNothing()

        obstacles = [(e["x"], e["y"]) for e in percept["entities"]
                     if e["looks_like"] == "wall"
                     or e["looks_like"] == "water"]
        players = [(e["x"], e["y"]) for e in percept["entities"]
                   if e["looks_like"] == "player"]
        missionaries = [(e["x"], e["y"]) for e in percept["entities"]
                        if e["looks_like"] == "coin"]
        cannibals = [(e["x"], e["y"]) for e in percept["entities"]
                     if e["looks_like"] == "evilCoin"]

        try:
            problem = PathfindingProblem(
                (0, 0), players, obstacles, [])
            a_star_graph(problem, get_heuristic(problem))
            return DoNothing()
        except NoSolutionError:
            pass

        reachable_missionary_count = 0
        for missionary in missionaries:
            try:
                problem = PathfindingProblem(
                    (0, 0), [missionary], obstacles, [])
                a_star_graph(problem, get_heuristic(problem))
                reachable_missionary_count += 1
            except NoSolutionError:
                pass

        reachable_cannibal_count = 0
        for cannibal in cannibals:
            try:
                problem = PathfindingProblem((0, 0), [cannibal], obstacles, [])
                a_star_graph(problem, get_heuristic(problem))
                reachable_cannibal_count += 1
            except NoSolutionError:
                pass

        if (reachable_cannibal_count + 1 > reachable_missionary_count
                and reachable_missionary_count > 0):
            if (-1, 0) in missionaries:
                return Attack(direction="left")
            elif (1, 0) in missionaries:
                return Attack(direction="right")
            elif (0, -1) in missionaries:
                return Attack(direction="down")
            elif (0, 1) in missionaries:
                return Attack(direction="up")
            problem = PathfindingProblem((0, 0), missionaries, obstacles, [])
            plan = a_star_graph(problem, get_heuristic(problem))
            return Move(direction=plan[0])
        return DoNothing()
