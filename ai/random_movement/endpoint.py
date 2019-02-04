import random


def next_move(percept):
    return random.choice(["move_up", "move_down", "move_left", "move_right"])


def reset():
    pass
