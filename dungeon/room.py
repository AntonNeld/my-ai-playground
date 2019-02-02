from entities.wall import Wall
from entities.player import Player
from entities.coin import Coin


class Room:

    def __init__(self):
        self._things = []

    def add_things(self, *things):
        for thing in things:
            if thing not in self._things:
                self._things.append(thing)
            else:
                raise RuntimeError("Cannot add thing twice: " + str(thing))

    def remove_things(self, *things):
        for thing in things:
            self._things.remove(thing)

    def get_things(self):
        return self._things.copy()

    def step(self):
        for thing in self._things:
            try:
                thing.step()
            except AttributeError:
                pass  # Fine if thing doesn't have step method.

    def is_wall(self, x, y):
        for thing in self._things:
            if thing.x == x and thing.y == y and thing.solid:
                return True

        return False


# Create a default room (just for testing)
default_room = Room()
default_room.add_things(Wall(0, 0), Wall(0, 1), Wall(0, 2), Wall(
    0, 3), Wall(0, 4), Wall(1, 2), Wall(3, 3), Player(5, 5), Coin(7, 7), Coin(7, 9), Coin(4, 12))
