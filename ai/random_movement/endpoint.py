import random


def next_move(state):
    return random.choice(["move_up", "move_down", "move_left", "move_right"])
