from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import Move


class RandomAI(BaseModel):
    kind: Literal["random"]

    def next_action(self, percept, random_generator):
        direction = random_generator.choice(["up", "down",
                                             "left", "right"])
        return Move(direction=direction)
