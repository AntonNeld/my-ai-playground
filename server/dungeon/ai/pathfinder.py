from typing import Dict, List, Union, Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.actions import DoNothing, Move
from dungeon.components import LooksLike
from .problems.pathfinding import PathfindingProblem, get_heuristic
from .search import (
    a_star_graph,
    a_star_tree,
    breadth_first_graph,
    breadth_first_tree,
    depth_first_graph,
    depth_first_tree,
    depth_first_tree_check_path,
    depth_limited_graph,
    depth_limited_tree,
    depth_limited_tree_check_path,
    greedy_best_first_graph,
    greedy_best_first_tree,
    iterative_deepening_graph,
    iterative_deepening_tree,
    iterative_deepening_tree_check_path,
    uniform_cost_graph,
    uniform_cost_tree,
    NoSolutionError
)


class PathfinderAI(BaseModel):
    kind: Literal["pathfinder"]
    obstacles: List[LooksLike] = []
    penalties: Dict[LooksLike, int] = {}
    goal: LooksLike
    algorithm: Union[
        Literal["aStarGraph"],
        Literal["aStarTree"],
        Literal["breadthFirstGraph"],
        Literal["breadthFirstTree"],
        Literal["depthFirstGraph"],
        Literal["depthFirstTree"],
        Literal["depthFirstTreeCheckPath"],
        Literal["depthLimitedGraph"],
        Literal["depthLimitedTree"],
        Literal["depthLimitedTreeCheckPath"],
        Literal["greedyBestFirstGraph"],
        Literal["greedyBestFirstTree"],
        Literal["iterativeDeepeningGraph"],
        Literal["iterativeDeepeningTree"],
        Literal["iterativeDeepeningTreeCheckPath"],
        Literal["uniformCostGraph"],
        Literal["uniformCostTree"],
    ] = "breadthFirstGraph"
    # This one is only used for depthLimitedGraph and depthLimitedTree
    depth_limit: Optional[int] = Field(None, alias="depthLimit")
    plan: Optional[List[str]]

    def update_state_percept(self, percept):
        if self.plan is None:
            goal = [(e["x"], e["y"]) for e in percept["entities"]
                    if e["looks_like"] == self.goal][0]
            obstacles = set(
                map(lambda e: (e["x"], e["y"]),
                    [e for e in percept["entities"]
                     if e["looks_like"] in self.obstacles]))
            penalties = {(e["x"], e["y"]): self.penalties[e["looks_like"]]
                         for e in percept["entities"]
                         if e["looks_like"] in self.penalties}
            problem = PathfindingProblem((0, 0), [goal], obstacles, penalties)
            try:
                if self.algorithm == "aStarGraph":
                    self.plan = a_star_graph(problem, get_heuristic(problem))
                elif self.algorithm == "aStarTree":
                    self.plan = a_star_tree(problem, get_heuristic(problem))
                elif self.algorithm == "breadthFirstGraph":
                    self.plan = breadth_first_graph(problem)
                elif self.algorithm == "breadthFirstTree":
                    self.plan = breadth_first_tree(problem)
                elif self.algorithm == "depthFirstGraph":
                    self.plan = depth_first_graph(problem)
                elif self.algorithm == "depthFirstTree":
                    self.plan = depth_first_tree(problem)
                elif self.algorithm == "depthFirstTreeCheckPath":
                    self.plan = depth_first_tree_check_path(problem)
                elif self.algorithm == "depthLimitedGraph":
                    self.plan = depth_limited_graph(problem, self.depth_limit)
                elif self.algorithm == "depthLimitedTree":
                    self.plan = depth_limited_tree(problem, self.depth_limit)
                elif self.algorithm == "depthLimitedTreeCheckPath":
                    self.plan = depth_limited_tree_check_path(
                        problem, self.depth_limit)
                elif self.algorithm == "greedyBestFirstGraph":
                    self.plan = greedy_best_first_graph(
                        problem, get_heuristic(problem))
                elif self.algorithm == "greedyBestFirstTree":
                    self.plan = greedy_best_first_tree(
                        problem, get_heuristic(problem))
                elif self.algorithm == "iterativeDeepeningGraph":
                    self.plan = iterative_deepening_graph(problem)
                elif self.algorithm == "iterativeDeepeningTree":
                    self.plan = iterative_deepening_tree(problem)
                elif self.algorithm == "iterativeDeepeningTreeCheckPath":
                    self.plan = iterative_deepening_tree_check_path(problem)
                elif self.algorithm == "uniformCostGraph":
                    self.plan = uniform_cost_graph(problem)
                elif self.algorithm == "uniformCostTree":
                    self.plan = uniform_cost_tree(problem)
            except NoSolutionError:
                self.plan = []

    def next_action(self, percept, random_generator):
        if self.plan:
            return Move(direction=self.plan[0])
        return DoNothing()

    def update_state_action(self, action):
        if action.action_type != "none":
            self.plan.pop(0)
