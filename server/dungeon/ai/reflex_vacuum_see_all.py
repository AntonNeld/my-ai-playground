from pydantic import BaseModel
from typing_extensions import Literal


class ReflexVacuumSeeAllAI(BaseModel):
    # Reflex vacuum cleaner agent from Figure 2.8
    kind: Literal["reflexVacuumSeeAll"]

    def next_move(self, percept):
        at_a = {"x": 0, "y": 0, "looks_like": "labelA"} in percept
        at_b = {"x": 0, "y": 0, "looks_like": "labelB"} in percept
        dirt_count = len([e for e in percept if e["looks_like"] == "dirt"])
        at_dirt = {"x": 0, "y": 0, "looks_like": "dirt"} in percept

        if at_dirt:
            return "pick_up"
        if at_a and dirt_count > 0:
            return "move_right"
        if at_b and dirt_count > 0:
            return "move_left"
        return "none"
