from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import Move, PickUp, DoNothing


class ReflexVacuumWithStateAI(BaseModel):
    # Reflex vacuum cleaner agent for exercise 2.10b
    kind: Literal["reflexVacuumWithState"]
    moved: bool = False

    def next_action(self, percept, random_generator):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return PickUp()
        if percept["position"]["x"] == 1 and not self.moved:
            return Move(direction="right")
        if percept["position"]["x"] == 2 and not self.moved:
            return Move(direction="left")
        return DoNothing()

    def update_state_action(self, action):
        if action.action_type == "move":
            self.moved = True
