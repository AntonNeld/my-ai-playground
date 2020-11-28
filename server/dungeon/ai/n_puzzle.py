import math
from collections import namedtuple
from typing import Optional, List

from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.actions import DoNothing, Move
from .search import iterative_deepening_graph, NoSolutionError

State = namedtuple("State", "empty_x empty_y numbers")


class NPuzzleProblem:

    def __init__(self, numbers):
        self.numbers = tuple(tuple(row) for row in numbers)
        self.size = len(numbers[0])

    def initial_state(self):
        for i, row in enumerate(self.numbers):
            if None in row:
                empty_y = i
                empty_x = row.index(None)
        return State(empty_x=empty_x, empty_y=empty_y, numbers=self.numbers)

    def actions(self, state):
        actions = ["up", "down", "left", "right"]
        if state.empty_x == 0:
            actions.remove("left")
        if state.empty_y == 0:
            actions.remove("down")
        if state.empty_x == self.size - 1:
            actions.remove("right")
        if state.empty_y == self.size - 1:
            actions.remove("up")
        return actions

    def result(self, state, action):
        old_x = state.empty_x
        old_y = state.empty_y
        numbers = [list(row) for row in state.numbers]
        if action == "left":
            new_x = old_x - 1
            new_y = old_y
        elif action == "right":
            new_x = old_x + 1
            new_y = old_y
        elif action == "up":
            new_x = old_x
            new_y = old_y + 1
        elif action == "down":
            new_x = old_x
            new_y = old_y - 1
        numbers[old_y][old_x] = numbers[new_y][new_x]
        numbers[new_y][new_x] = None
        return State(empty_x=new_x, empty_y=new_y,
                     numbers=tuple(tuple(row) for row in numbers))

    def goal_test(self, state):
        if state.empty_x != self.size - 1 or state.empty_y != 0:
            return False
        flat_numbers = [
            n for row in reversed(state.numbers) for n in row if n is not None]
        # Check if sorted
        return all(flat_numbers[i] < flat_numbers[i+1]
                   for i in range(len(flat_numbers)-1))

    def step_cost(self, state, action, result):
        return 1


class NPuzzleAI(BaseModel):
    kind: Literal["nPuzzle"]
    plan: Optional[List[str]]

    def update_state_percept(self, percept):
        if self.plan is None:
            number_entities = [e for e in percept["entities"]
                               if e["looks_like"] != "wall"]
            numbers_with_player = number_entities + [{"x": 0, "y": 0}]
            problem_size = int(math.sqrt(len(numbers_with_player)))
            sorted_by_y = sorted(numbers_with_player, key=lambda e: e["y"])
            numbers = []
            for i in range(0, len(numbers_with_player), problem_size):
                on_this_row = sorted_by_y[i:i+problem_size]
                numbers.append(
                    [
                        int(e["looks_like"].replace("label:", ""))
                        if "looks_like" in e else None
                        for e in sorted(on_this_row, key=lambda e: e["x"])
                    ]
                )
            problem = NPuzzleProblem(numbers)
            try:
                self.plan = iterative_deepening_graph(
                    problem, iteration_limit=200000)
            except NoSolutionError:
                self.plan = []

    def next_action(self, percept, random_generator):
        if not self.plan:
            return DoNothing()
        return Move(direction=self.plan[0])

    def update_state_action(self, action):
        if self.plan:
            self.plan.pop(0)
