from pydantic import BaseModel
from typing_extensions import Literal


class ReflexVacuumSeeAllAI(BaseModel):
    # Reflex vacuum cleaner agent from Figure 2.8
    kind: Literal["reflexVacuumSeeAll"]

    def next_action(self, percept):
        dirt_count = len([e for e in percept["entities"]
                          if e["looks_like"] == "dirt"])

        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return "pick_up"
        if percept["position"]["x"] == 1 and dirt_count > 0:
            return "move_right"
        if percept["position"]["x"] == 2 and dirt_count > 0:
            return "move_left"
        return "none"
