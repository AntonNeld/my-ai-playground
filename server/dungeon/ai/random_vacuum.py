import random

from pydantic import BaseModel
from typing_extensions import Literal


class RandomVacuumAI(BaseModel):
    # Random vacuum agent from exercise 2.11bc
    kind: Literal["randomVacuum"]

    def next_move(self, percept):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return "pick_up"
        return random.choice(["move_up", "move_down",
                              "move_left", "move_right"])
