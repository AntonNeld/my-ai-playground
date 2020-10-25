from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import Move, PickUp


class RandomVacuumAI(BaseModel):
    # Random vacuum agent from exercise 2.11bc
    kind: Literal["randomVacuum"]

    def next_action(self, percept, random_generator):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return PickUp()
        direction = random_generator.choice(["up", "down",
                                             "left", "right"])
        return Move(direction=direction)
