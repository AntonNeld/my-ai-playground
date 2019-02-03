import pytmx
from entities.wall import Wall
from entities.player import Player
from entities.coin import Coin

current_room = None


class Room:

    def __init__(self):
        self._things = []
        self.score = self.steps = 0

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

    def get_view(self):
        to_return = {"score": self.score,
                     "steps": self.steps}
        serializables = []
        things = self.get_things()
        for thing in things:
            serializable = {"x":          thing.x,
                            "y":          thing.y,
                            "looks_like": thing.looks_like}
            serializables.append(serializable)

        to_return["things"] = serializables
        return to_return

    def step(self):
        for thing in self._things:
            if hasattr(thing, "step"):
                thing.step()

    def is_wall(self, x, y):
        for thing in self._things:
            if thing.x == x and thing.y == y and thing.solid:
                return True

        return False


def create_room_from_tilemap(path):
    new_room = Room()
    tiledata = pytmx.TiledMap(path)
    for layer in tiledata.layers:
        thing_type = layer.properties["Type"]
        for (x, inverted_y, gid) in layer.iter_data():
            y = tiledata.height - inverted_y - 1
            if gid != 0:
                if thing_type == "block":
                    new_room.add_things(Wall(x, y))
                elif thing_type == "player":
                    new_room.add_things(Player(x, y))
                elif thing_type == "coin":
                    new_room.add_things(Coin(x, y))
    return new_room


def set_current_room(room):
    global current_room
    current_room = room


def get_current_room():
    return current_room
