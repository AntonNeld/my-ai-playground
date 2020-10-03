import random

from pydantic import BaseModel
from typing_extensions import Literal


class RandomVacuumAI(BaseModel):
    # Random vacuum agent from exercise 2.11bc
    kind: Literal["randomVacuum"]
    seed: int

    def next_action(self, percept):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return "pick_up"
        generator = random.Random(self.seed)
        action = generator.choice(["move_up", "move_down",
                                   "move_left", "move_right"])
        self.seed = hash(generator.getstate())
        return action
