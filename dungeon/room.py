import os
from os.path import abspath, dirname, join
import requests
import pytmx
from entities.wall import Wall
from entities.player import Player
from entities.coin import Coin

current_room = None

if "DUNGEON_MAP" in os.environ:
    MAP = os.environ["DUNGEON_MAP"]
else:
    MAP = "default"

if "DUNGEON_PLAYER_AI" in os.environ:
    ai_host = os.environ["DUNGEON_PLAYER_AI"]
else:
    ai_host = "127.0.0.1"
RESET_AI_URL = "http://" + ai_host + ":5100/api/reset"


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

    def get_view(self, perceptor=None):
        if perceptor:
            x = perceptor.x
            y = perceptor.y
        else:
            x = y = 0
        to_return = {"score": self.score,
                     "steps": self.steps}
        serializables = []
        things = self.get_things()
        for thing in things:
            if thing != perceptor:
                serializable = {"x":          thing.x - x,
                                "y":          thing.y - y,
                                "looks_like": thing.looks_like}
                serializables.append(serializable)

        to_return["things"] = serializables
        return to_return

    def step(self):
        for thing in self._things:
            if hasattr(thing, "step"):
                thing.step()

    def passable(self, x, y):
        for thing in self.get_things():
            if thing.x == x and thing.y == y and thing.solid:
                return False
        return True


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


def init_room():
    try:
        requests.put(RESET_AI_URL)
    except requests.exceptions.ConnectionError:
        pass  # Probably just not started
    set_current_room(create_room_from_tilemap(
        join(dirname(abspath(__file__)), "maps", MAP + ".tmx")))
