from ai import pathfinder
from ai import manual
from ai import random

ai_types = {"pathfinder": pathfinder, "manual": manual, "random": random}


def next_move(ai, agent, percept):
    return ai_types[ai].next_move(agent, percept)


def manual_set_move(agent, action):
    manual.set_move(agent, action)


def delete(ai, agent):
    ai_types[ai].delete(agent)
