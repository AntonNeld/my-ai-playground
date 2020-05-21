from ais import ai_types
from entities.wall import Wall
from entities.player import Player
from entities.coin import Coin

rooms = {}


class Room:

    def __init__(self):
        self._things = []
        self.steps = 0
        self._agents = []

    def add_things(self, *things):
        for thing in things:
            if thing not in self._things:
                self._things.append(thing)
            else:
                raise RuntimeError("Cannot add thing twice: " + str(thing))
            if isinstance(thing, Player):
                self._agents.append(thing)

    def remove_things(self, *things):
        for thing in things:
            self._things.remove(thing)
            if thing in self._agents:
                self._agents.remove(thing)

    def get_things(self):
        return self._things.copy()

    def get_agents(self):
        return self._agents.copy()

    def get_view(self, perceptor=None, include_id=False):
        if perceptor:
            x = perceptor.x
            y = perceptor.y
        else:
            x = y = 0
        serializables = []
        things = self.get_things()
        for thing in things:
            if thing != perceptor:
                serializable = {"x":          thing.x - x,
                                "y":          thing.y - y,
                                "looks_like": thing.looks_like}
                if include_id:
                    serializable["id"] = thing.id
                serializables.append(serializable)

        return serializables

    def step(self):
        actions = {}
        for agent in self._agents:
            actions[agent] = ai_types[agent.ai].next_move(
                agent.id, self.get_view(agent))
        for thing in self._things:
            if hasattr(thing, "step"):
                if thing in actions:
                    thing.step(actions[thing])
                else:
                    thing.step()
        self.steps += 1

    def passable(self, x, y):
        for thing in self.get_things():
            if thing.x == x and thing.y == y and thing.solid:
                return False
        return True


def create_room_from_list(data):
    new_room = Room()
    for thing in data:
        x = thing["x"]
        y = thing["y"]
        if thing["type"] == "block":
            new_room.add_things(Wall(new_room, x, y))
        elif thing["type"] == "player":
            new_room.add_things(Player(new_room, x, y, thing["ai"]))
        elif thing["type"] == "coin":
            new_room.add_things(Coin(new_room, x, y))
    return new_room


def get_room(room_id):
    try:
        return rooms[room_id]
    except KeyError:
        return None


def delete_room(room_id):
    current = get_room(room_id)
    if current:
        for agent in current.get_agents():
            ai_types[agent.ai].delete(agent.id)
        del rooms[room_id]


def init_room(room_id, data):
    delete_room(room_id)
    rooms[room_id] = create_room_from_list(data)
