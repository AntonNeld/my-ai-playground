from dungeon.entities.wall import Wall
from dungeon.entities.player import Player
from dungeon.entities.coin import Coin
from dungeon.ai import PathfinderAI, ManualAI, RandomAI, ExhaustiveAI


class Room:

    def __init__(self):
        self._entities = []
        self.steps = 0

    def add_entities(self, *entities):
        for entity in entities:
            if entity not in self._entities:
                self._entities.append(entity)
            else:
                raise RuntimeError("Cannot add entity twice: " + str(entity))

    def remove_entities(self, *entities):
        for entity in entities:
            self._entities.remove(entity)

    def get_entities(self):
        return self._entities.copy()

    def get_agents(self):
        return [entity for entity in self._entities if hasattr(entity, "ai")]

    def get_view(self, perceptor=None, include_id=False):
        if perceptor:
            x = perceptor.x
            y = perceptor.y
        else:
            x = y = 0
        serializables = []
        entities = self.get_entities()
        for entity in entities:
            if entity != perceptor:
                serializable = {"x":          entity.x - x,
                                "y":          entity.y - y,
                                "looks_like": entity.looks_like}
                if include_id:
                    serializable["id"] = entity.id
                serializables.append(serializable)

        return serializables

    def step(self):
        for entity in self._entities:
            if hasattr(entity, "step"):
                if hasattr(entity, "ai"):
                    action = entity.ai.next_move(self.get_view(entity))
                    entity.step(action)
                else:
                    entity.step()
        self.steps += 1

    def passable(self, x, y):
        for entity in self.get_entities():
            if entity.x == x and entity.y == y and entity.solid:
                return False
        return True

    def to_json(self):
        return [entity.to_json() for entity in self._entities]


def create_room_from_list(data):
    new_room = Room()
    for entity in data:
        x = entity["x"]
        y = entity["y"]
        if entity["type"] == "block":
            new_room.add_entities(Wall(new_room, x, y))
        elif entity["type"] == "player":
            if entity["ai"] == "pathfinder":
                ai = PathfinderAI()
            elif entity["ai"] == "manual":
                ai = ManualAI()
            elif entity["ai"] == "random":
                ai = RandomAI()
            elif entity["ai"] == "exhaustive":
                ai = ExhaustiveAI()
            else:
                raise RuntimeError(f"Unknown AI {entity['ai']}")
            new_room.add_entities(Player(new_room, x, y, ai))
        elif entity["type"] == "coin":
            new_room.add_entities(Coin(new_room, x, y))
    return new_room
