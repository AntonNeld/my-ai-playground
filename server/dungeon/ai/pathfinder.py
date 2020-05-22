import math

from dungeon.ai.lib.perception import get_coordinates
from dungeon.ai.lib.pathfinding import breadth_first


class PathfinderAI:

    def __init__(self):
        self._plan = []

    def next_move(self, percept):
        if not self._plan:
            walls = get_coordinates(percept, "wall")
            coins = get_coordinates(percept, "coin")
            shortest = math.inf
            for coin in coins:
                new_actions = breadth_first((0, 0), coin, walls)
                if new_actions and len(new_actions) < shortest:
                    self._plan = new_actions
                    shortest = len(new_actions)
            if shortest == math.inf:
                self._plan = ["none"]
        return self._plan.pop(0)

    def to_json(self):
        return "pathfinder"
