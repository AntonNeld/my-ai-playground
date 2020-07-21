from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import Move


class SingularAI(BaseModel):
    kind: Literal["singular"]
    move: Move

    def next_move(self, percept):
        return self.move
