from typing import Dict, List, Union, Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.consts import LooksLike, Move
from dungeon.ai.lib.search import (
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


class PathfindingProblem:

    def __init__(self, start, goal, obstacles, penalties):
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.penalties = penalties

    def initial_state(self):
        return self.start

    def actions(self, state):
        actions = []
        x = state[0]
        y = state[1]
        if (x, y+1) not in self.obstacles:
            actions.append("move_up")
        if (x, y-1) not in self.obstacles:
            actions.append("move_down")
        if (x+1, y) not in self.obstacles:
            actions.append("move_right")
        if (x-1, y) not in self.obstacles:
            actions.append("move_left")
        return actions

    def result(self, state, action):
        x = state[0]
        y = state[1]
        if action == "move_up":
            return (x, y+1)
        if action == "move_down":
            return (x, y-1)
        if action == "move_right":
            return (x+1, y)
        if action == "move_left":
            return (x-1, y)
        return (x, y)

    def goal_test(self, state):
        return state == self.goal

    def step_cost(self, state, action, result):
        if result in self.penalties:
            return 1 + self.penalties[result]
        return 1


def get_heuristic(problem):
    def heuristic(node):
        return (abs(problem.goal[0] - node.state[0])
                + abs(problem.goal[1] - node.state[1]))
    return heuristic


class PathfinderAI(BaseModel):
    kind: Literal["pathfinder"]
    obstacles: List[LooksLike] = []
    penalties: Dict[LooksLike, int] = {}
    goal: LooksLike
    algorithm: Union[
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
    plan: Optional[List[Move]]

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
            problem = PathfindingProblem((0, 0), goal, obstacles, penalties)
            try:
                if self.algorithm == "breadthFirstGraph":
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

    def next_move(self, percept):
        if self.plan:
            return self.plan[0]
        return "none"

    def update_state_action(self, action):
        if action != "none":
            self.plan.pop(0)
