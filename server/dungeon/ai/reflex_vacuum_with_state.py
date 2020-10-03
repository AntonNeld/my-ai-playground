from pydantic import BaseModel
from typing_extensions import Literal


class ReflexVacuumWithStateAI(BaseModel):
    # Reflex vacuum cleaner agent for exercise 2.10b
    kind: Literal["reflexVacuumWithState"]
    moved: bool = False

    def next_action(self, percept):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return "pick_up"
        if percept["position"]["x"] == 1 and not self.moved:
            return "move_right"
        if percept["position"]["x"] == 2 and not self.moved:
            return "move_left"
        return "none"

    def update_state_action(self, action):
        if action in ["move_left", "move_right"]:
            self.moved = True
