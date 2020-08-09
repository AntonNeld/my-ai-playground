from pydantic import BaseModel
from typing_extensions import Literal


class ReflexVacuumWithStateAI(BaseModel):
    # Reflex vacuum cleaner agent for exercise 2.10b
    kind: Literal["reflexVacuumWithState"]
    moved: bool

    def next_move(self, percept):
        view = list(map(lambda e: e["looks_like"], percept["entities"]))
        if "dirt" in view:
            return "pick_up"
        if "labelA" in view and not self.moved:
            return "move_right"
        if "labelB" in view and not self.moved:
            return "move_left"
        return "none"

    def update_state_action(self, action):
        if action in ["move_left", "move_right"]:
            self.moved = True
