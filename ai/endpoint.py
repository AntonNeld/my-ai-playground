import importlib
import os
from os import path

# Dynamically import all modules from ai/ into ai_types
ai_types = {}
for f in os.listdir(path.join(path.dirname(__file__), "ais")):
    module = f.replace(".py", "")
    ai_types[module] = importlib.import_module("ais.{}".format(module))


def next_move(ai, agent, percept):
    return ai_types[ai].next_move(agent, percept)


def manual_set_move(agent, action):
    ai_types["manual"].set_move(agent, action)


def delete(ai, agent):
    ai_types[ai].delete(agent)
