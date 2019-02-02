from entities.wall import Wall
from entities.player import Player


class Room:

    def __init__(self):
        self._things = []

    def add_things(self, *things):
        for thing in things:
            if thing not in self._things:
                self._things.append(thing)
            else:
                raise RuntimeError("Cannot add thing twice: " + str(thing))

    def get_things(self):
        return self._things.copy()

    def step(self):
        for thing in self._things:
            try:
                thing.step()
            except AttributeError:
                pass  # Fine if thing doesn't have step method.


# Create a default room (just for testing)
default_room = Room()
default_room.add_things(Wall(0, 0), Wall(0, 1), Wall(0, 2), Wall(
    0, 3), Wall(0, 4), Wall(1, 2), Wall(3, 3), Player(2, 2))
