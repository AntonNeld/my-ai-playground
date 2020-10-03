from pydantic import BaseModel
from typing_extensions import Literal


class ReflexVacuumAgentAI(BaseModel):
    # Reflex vacuum cleaner agent from Figure 2.8
    kind: Literal["reflexVacuumAgent"]

    def next_action(self, percept):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return "pick_up"
        if percept["position"]["x"] == 1:
            return "move_right"
        if percept["position"]["x"] == 2:
            return "move_left"
        return "none"
