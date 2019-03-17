from pathfinder import endpoint as pathfinder
from manual import endpoint as manual
from random_movement import endpoint as random_movement


def next_move(ai, agent, percept):
    if ai == "pathfinder":
        return pathfinder.next_move(agent, percept)
    if ai == "manual":
        return manual.next_move(agent, percept)
    if ai == "random":
        return random_movement.next_move(agent, percept)


def manual_set_move(agent, action):
    manual.set_move(action)


def delete(ai, agent):
    if ai == "pathfinder":
        pathfinder.delete(agent)
    if ai == "manual":
        manual.delete(agent)
    if ai == "random":
        random_movement.delete(agent)
