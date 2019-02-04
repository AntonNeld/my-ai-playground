import math

from perception import get_coordinates
from pathfinding import breadth_first

actions = []


def next_move(percept):
    global actions
    if not actions:
        walls = get_coordinates(percept, "wall")
        coins = get_coordinates(percept, "coin")
        if not coins:
            return "none"
        shortest = math.inf
        for coin in coins:
            new_actions = breadth_first((0, 0), coin, walls)
            if new_actions and len(new_actions) < shortest:
                actions = new_actions
                shortest = len(new_actions)
        if not actions:
            actions = ["none"]
    return actions.pop(0)
