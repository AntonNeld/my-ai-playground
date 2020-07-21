
from typing import Optional

from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import Move


class ManualAI(BaseModel):
    kind: Literal["manual"]
    plan: Optional[Move]

    def next_move(self, percept):
        action = self.plan
        self.plan = "none"
        return action if action is not None else "none"

    def set_move(self, action):
        self.plan = action
