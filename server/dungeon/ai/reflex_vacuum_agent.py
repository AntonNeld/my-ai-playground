from pydantic import BaseModel
from typing_extensions import Literal


class ReflexVacuumAgentAI(BaseModel):
    # Reflex vacuum cleaner agent from Figure 2.8
    kind: Literal["reflexVacuumAgent"]

    def next_move(self, percept):
        view = list(map(lambda e: e["looks_like"], percept))
        if "dirt" in view:
            return "pick_up"
        if "labelA" in view:
            return "move_right"
        if "labelB" in view:
            return "move_left"
        return "none"
