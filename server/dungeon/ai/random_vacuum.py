import random

from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import Move, PickUp


class RandomVacuumAI(BaseModel):
    # Random vacuum agent from exercise 2.11bc
    kind: Literal["randomVacuum"]
    seed: int

    def next_action(self, percept):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return PickUp()
        generator = random.Random(self.seed)
        direction = generator.choice(["up", "down",
                                      "left", "right"])
        self.seed = hash(generator.getstate())
        return Move(direction=direction)
