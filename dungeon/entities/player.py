import rooms
from .coin import Coin
from .entity import Entity


class Player(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, "player")
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

        if rooms.get_current_room().passable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

        for thing in rooms.get_current_room().get_things():
            if (isinstance(thing, Coin) and thing.x == self.x
                    and thing.y == self.y):
                rooms.get_current_room().remove_things(thing)
                self.score += 1
