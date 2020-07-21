import random

from pydantic import BaseModel
from typing_extensions import Literal


class RandomAI(BaseModel):
    kind: Literal["random"]

    def next_move(agent, percept):
        return random.choice(["move_up", "move_down",
                              "move_left", "move_right"])
