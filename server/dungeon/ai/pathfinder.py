import math
from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.ai.lib.perception import get_coordinates
from dungeon.ai.lib.pathfinding import breadth_first
from models import Move


class PathfinderAI(BaseModel):
    kind: Literal["pathfinder"]
    plan: Optional[List[Move]]

    def next_move(self, percept):
        if not self.plan:
            walls = get_coordinates(percept, "wall")
            coins = get_coordinates(percept, "coin")
            shortest = math.inf
            for coin in coins:
                new_actions = breadth_first((0, 0), coin, walls)
                if new_actions and len(new_actions) < shortest:
                    self.plan = new_actions
                    shortest = len(new_actions)
            if shortest == math.inf:
                self.plan = ["none"]
        return self.plan.pop(0)
