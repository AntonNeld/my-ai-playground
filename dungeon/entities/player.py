import uuid

import room
from .coin import Coin


class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.looks_like = "player"
        self.id = uuid.uuid4().hex
        self.solid = True
        self.score = 0

    def step(self, action="none"):
        dx = dy = 0

        if action == "move_up":
            dy = 1
        elif action == "move_down":
            dy = -1
        elif action == "move_left":
            dx = -1
        elif action == "move_right":
            dx = 1

        if room.get_current_room().passable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

        for thing in room.get_current_room().get_things():
            if (isinstance(thing, Coin) and thing.x == self.x
                    and thing.y == self.y):
                room.get_current_room().remove_things(thing)
                self.score += 1
