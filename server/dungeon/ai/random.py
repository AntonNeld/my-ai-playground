import random

from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import Move


class RandomAI(BaseModel):
    kind: Literal["random"]
    seed: int

    def next_action(self, percept):
        generator = random.Random(self.seed)
        direction = generator.choice(["up", "down",
                                      "left", "right"])
        self.seed = hash(generator.getstate())
        return Move(direction=direction)
