from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.consts import Action


class SingularAI(BaseModel):
    kind: Literal["singular"]
    action: Action

    def next_action(self, percept):
        return self.action
