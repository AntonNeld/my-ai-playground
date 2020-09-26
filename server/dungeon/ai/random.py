import random

from pydantic import BaseModel
from typing_extensions import Literal


class RandomAI(BaseModel):
    kind: Literal["random"]
    seed: int

    def next_move(self, percept):
        generator = random.Random(self.seed)
        move = generator.choice(["move_up", "move_down",
                                 "move_left", "move_right"])
        self.seed = hash(generator.getstate())
        return move
