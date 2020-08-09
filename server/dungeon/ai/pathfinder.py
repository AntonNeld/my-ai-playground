from typing import List

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.ai.lib.perception import get_coordinates
from dungeon.ai.lib.pathfinding import shortest_breadth_first
from dungeon.consts import Move


class PathfinderAI(BaseModel):
    kind: Literal["pathfinder"]
    manual_pickup: bool = Field(False, alias="manualPickup")
    plan: List[Move] = []

    def next_move(self, percept):
        if (self.manual_pickup and {"x": 0, "y": 0, "looks_like": "coin"}
                in percept["entities"]):
            return "pick_up"

        if not self.plan:
            walls = get_coordinates(percept["entities"], "wall")
            coins = get_coordinates(percept["entities"], "coin")
            self.plan = shortest_breadth_first((0, 0), coins, walls)

        return self.plan.pop(0)
