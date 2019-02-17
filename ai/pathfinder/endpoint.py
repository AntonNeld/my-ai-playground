import math

from perception import get_coordinates
from pathfinding import breadth_first

actions = {}


def next_move(agent, percept):
    if agent not in actions or not actions[agent]:
        walls = get_coordinates(percept, "wall")
        coins = get_coordinates(percept, "coin")
        if not coins:
            return "none"
        shortest = math.inf
        for coin in coins:
            new_actions = breadth_first((0, 0), coin, walls)
            if new_actions and len(new_actions) < shortest:
                actions[agent] = new_actions
                shortest = len(new_actions)
        if shortest == math.inf:
            actions[agent] = ["none"]
    return actions[agent].pop(0)


def delete(agent):
    del actions[agent]
