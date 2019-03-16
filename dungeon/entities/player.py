from .coin import Coin
from .entity import Entity


class Player(Entity):

    def __init__(self, room, x, y):
        super().__init__(room, x, y, "player")
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

        if self.room.passable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

        for thing in self.room.get_things():
            if (isinstance(thing, Coin) and thing.x == self.x
                    and thing.y == self.y):
                self.room.remove_things(thing)
                self.score += 1
