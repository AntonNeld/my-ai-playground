import random


class RandomAI:
    def next_move(agent, percept):
        return random.choice(["move_up", "move_down",
                              "move_left", "move_right"])

    def to_dict(self):
        return {"kind": "random"}
