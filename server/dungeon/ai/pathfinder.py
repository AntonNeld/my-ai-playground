import math
from typing import List

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.ai.lib.perception import get_coordinates
from dungeon.ai.lib.pathfinding import breadth_first
from dungeon.consts import Move


class PathfinderAI(BaseModel):
    kind: Literal["pathfinder"]
    manual_pickup: bool = Field(False, alias="manualPickup")
    plan: List[Move] = []

    def next_move(self, percept):
        if not self.plan:
            walls = get_coordinates(percept["entities"], "wall")
            coins = get_coordinates(percept["entities"], "coin")
            shortest = math.inf
            for coin in coins:
                new_actions = breadth_first((0, 0), coin, walls)
                if new_actions and len(new_actions) < shortest:
                    self.plan = new_actions
                    shortest = len(new_actions)
            if self.manual_pickup:
                self.plan.append("pick_up")
            if shortest == math.inf:
                self.plan = ["none"]
        return self.plan.pop(0)
