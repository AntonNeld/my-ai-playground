import json

current_action = "none"


def next_move(state):
    return current_action


def set_move(action):
    global current_action
    current_action = action