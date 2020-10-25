from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import Move, PickUp, DoNothing


class ReflexVacuumAgentAI(BaseModel):
    # Reflex vacuum cleaner agent from Figure 2.8
    kind: Literal["reflexVacuumAgent"]

    def next_action(self, percept, random_generator):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return PickUp()
        if percept["position"]["x"] == 1:
            return Move(direction="right")
        if percept["position"]["x"] == 2:
            return Move(direction="left")
        return DoNothing()
