from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.ai.lib.perception import get_coordinates
from dungeon.ai.lib.pathfinding import shortest_breadth_first


class GetNearestCoinAI(BaseModel):
    kind: Literal["getNearestCoin"]
    manual_pickup: bool = Field(False, alias="manualPickup")

    def next_move(self, percept):
        if (self.manual_pickup and {"x": 0, "y": 0, "looks_like": "coin"}
                in percept["entities"]):
            return "pick_up"

        walls = get_coordinates(percept["entities"], "wall")
        coins = get_coordinates(percept["entities"], "coin")
        plan = shortest_breadth_first((0, 0), coins, walls)

        return plan[0]
