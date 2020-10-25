from collections import namedtuple
from typing import Optional, List, Union

from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import DoNothing, Move, Drop, PickUp
from .search import breadth_first_graph, a_star_graph
from .problems.pathfinding import PathfindingProblem, get_heuristic

People = namedtuple("People", "missionaries cannibals")
State = namedtuple("State", "first_shore second_shore boat_location")


class MissionariesAndCannibalsProblem:

    def initial_state(self):
        return State(
            first_shore=People(missionaries=3, cannibals=3),
            second_shore=People(missionaries=0, cannibals=0),
            boat_location="first_shore"
        )

    def actions(self, state):
        actions = []
        for action in [
            People(missionaries=1, cannibals=0),
            People(missionaries=2, cannibals=0),
            People(missionaries=0, cannibals=1),
            People(missionaries=0, cannibals=2),
            People(missionaries=1, cannibals=1),
        ]:
            result = self.result(state, action)
            if self._permissible_state(result):
                actions.append(action)
        return actions

    def _permissible_state(self, state):
        for shore_index in [0, 1]:
            missionaries = state[shore_index].missionaries
            cannibals = state[shore_index].cannibals
            if cannibals < 0 or missionaries < 0:
                return False
            if missionaries > 0 and cannibals > missionaries:
                return False
        return True

    def result(self, state, action):
        old_boat_location = state.boat_location
        if old_boat_location == "first_shore":
            new_boat_location = "second_shore"
            old_shore_index = 0
            new_shore_index = 1
        else:
            new_boat_location = "first_shore"
            old_shore_index = 1
            new_shore_index = 0

        missionaries_here = state[old_shore_index].missionaries
        cannibals_here = state[old_shore_index].cannibals
        missionaries_there = state[new_shore_index].missionaries
        cannibals_there = state[new_shore_index].cannibals

        return State(boat_location=new_boat_location, **{
            old_boat_location: People(
                missionaries=missionaries_here - action.missionaries,
                cannibals=cannibals_here - action.cannibals
            ),
            new_boat_location: People(
                missionaries=missionaries_there + action.missionaries,
                cannibals=cannibals_there + action.cannibals
            )
        })

    def goal_test(self, state):
        return state.second_shore == People(missionaries=3, cannibals=3)

    def step_cost(self, state, action, result):
        return 1


class HighLevelGoal(BaseModel):
    missionaries: int
    cannibals: int
    destination: Union[Literal["dirt"], Literal["grass"]]


class MissionariesAndCannibalsAI(BaseModel):
    # Missionaries and cannibals, exercise 3.9
    # It's taking the optimal number of trips, but not
    # necessarily the fewest steps
    kind: Literal["missionariesAndCannibals"]
    plan: Optional[List[HighLevelGoal]]

    def update_state_percept(self, percept):
        if self.plan is None:
            problem = MissionariesAndCannibalsProblem()
            plan = breadth_first_graph(problem)
            self.plan = [
                HighLevelGoal(
                    missionaries=a.missionaries,
                    cannibals=a.cannibals,
                    destination=("grass"
                                 if i % 2 == 0 else "dirt")
                )
                for i, a in enumerate(plan)
            ]
            self.plan.append(HighLevelGoal(
                missionaries=0, cannibals=0, destination="grass"))
        # Check if we have reached the current goal
        if self.plan:
            goal = self.plan[0]
            inventory = percept["inventory"]
            if (
                inventory.count("coin") == goal.missionaries
                and inventory.count("evilCoin") == goal.cannibals
                and {"x": 0, "y": 0, "looks_like": goal.destination}
                in percept["entities"]
            ):
                self.plan.pop(0)

    def next_action(self, percept, random_generator):
        if not self.plan:
            return DoNothing()

        # Parse percept
        missionaries = set((e["x"], e["y"])
                           for e in percept["entities"]
                           if e["looks_like"] == "coin")
        cannibals = set((e["x"], e["y"])
                        for e in percept["entities"]
                        if e["looks_like"] == "evilCoin")
        grass = set((e["x"], e["y"])
                    for e in percept["entities"]
                    if e["looks_like"] == "grass")
        dirt = set((e["x"], e["y"])
                   for e in percept["entities"]
                   if e["looks_like"] == "dirt")
        empty_shore = (grass | dirt) - missionaries - cannibals
        walls = set((e["x"], e["y"])
                    for e in percept["entities"]
                    if e["looks_like"] == "wall")
        water = set((e["x"], e["y"])
                    for e in percept["entities"]
                    if e["looks_like"] == "water")
        goal = self.plan[0]
        # First, ensure inventory is correct
        too_many_missionaries = percept["inventory"].count(
            "coin") > goal.missionaries
        too_many_cannibals = percept["inventory"].count(
            "evilCoin") > goal.cannibals
        if too_many_missionaries or too_many_cannibals:

            if (0, 0) in empty_shore:
                if too_many_missionaries:
                    return Drop(index=percept["inventory"].index("coin"))
                if too_many_cannibals:
                    return Drop(index=percept["inventory"].index("evilCoin"))

            problem = PathfindingProblem(
                (0, 0), empty_shore, walls | water, [])
            return Move(direction=a_star_graph(problem,
                                               get_heuristic(problem))[0])

        too_few_missionaries = percept["inventory"].count(
            "coin") < goal.missionaries
        if too_few_missionaries:
            if (0, 0) in missionaries:
                return PickUp()
            problem = PathfindingProblem(
                (0, 0), missionaries, walls | water, [])
            return Move(direction=a_star_graph(problem,
                                               get_heuristic(problem))[0])

        too_few_cannibals = percept["inventory"].count(
            "evilCoin") < goal.cannibals
        if too_few_cannibals:
            if (0, 0) in cannibals:
                return PickUp()
            problem = PathfindingProblem(
                (0, 0), cannibals, walls | water, [])
            return Move(direction=a_star_graph(problem,
                                               get_heuristic(problem))[0])

        # Then, go to the correct shore
        if goal.destination == "dirt":
            problem = PathfindingProblem((0, 0), dirt, walls, [])
            return Move(direction=a_star_graph(problem,
                                               get_heuristic(problem))[0])
        else:
            problem = PathfindingProblem((0, 0), grass, walls, [])
            return Move(direction=a_star_graph(problem,
                                               get_heuristic(problem))[0])
