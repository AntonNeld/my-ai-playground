from typing import List

from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import LooksLike, Position
from dungeon.ai.lib.search import breadth_first_graph, NoSolutionError


class PathfindingProblem:

    def __init__(self, start, goal, obstacles):
        self.start = start
        self.goal = goal
        self.obstacles = obstacles

    def initial_state(self):
        return self.start

    def actions(self, state):
        actions = set()
        x = state[0]
        y = state[1]
        if (x, y+1) not in self.obstacles:
            actions.add("move_up")
        if (x, y-1) not in self.obstacles:
            actions.add("move_down")
        if (x+1, y) not in self.obstacles:
            actions.add("move_right")
        if (x-1, y) not in self.obstacles:
            actions.add("move_left")
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
        return 1


class PathfinderAI(BaseModel):
    kind: Literal["pathfinder"]
    obstacles: List[LooksLike]
    goal: Position

    def next_move(self, percept):
        obstacles = set(
            map(lambda e: (e["x"], e["y"]),
                [e for e in percept["entities"]
                 if e["looks_like"] in self.obstacles]))
        problem = PathfindingProblem(
            (0, 0), (self.goal.x, self.goal.y), obstacles)
        try:
            solution = breadth_first_graph(problem)
            if len(solution) == 0:
                return "none"
            return solution[0]
        except NoSolutionError:
            return "none"

    def update_state_action(self, action):
        if action == "move_up":
            self.goal.y -= 1
        if action == "move_down":
            self.goal.y += 1
        if action == "move_right":
            self.goal.x -= 1
        if action == "move_left":
            self.goal.x += 1
