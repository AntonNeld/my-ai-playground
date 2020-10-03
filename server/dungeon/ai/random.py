import random

from pydantic import BaseModel
from typing_extensions import Literal


class RandomAI(BaseModel):
    kind: Literal["random"]
    seed: int

    def next_action(self, percept):
        generator = random.Random(self.seed)
        action = generator.choice(["move_up", "move_down",
                                   "move_left", "move_right"])
        self.seed = hash(generator.getstate())
        return action
