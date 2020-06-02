import uuid

from errors import ResourceNotFoundError
from dungeon.entities.entity_factories import entity_from_dict


class Room:

    def __init__(self, steps):
        self._entities = {}
        self.steps = steps

    def add_entity(self, entity, entity_id=None):
        entity.set_room(self)
        if entity_id is None:
            entity_id = uuid.uuid4().hex
        self._entities[entity_id] = entity
        return entity_id

    def remove_entity(self, entity):
        id_to_remove = None
        for entity_id, entity_object in self._entities.items():
            if entity_object == entity:
                id_to_remove = entity_id
        del self._entities[id_to_remove]

    def remove_entity_by_id(self, entity_id):
        if entity_id in self._entities:
            del self._entities[entity_id]

    def list_entities(self):
        return list(self._entities.keys())

    def get_entity(self, entity_id):
        try:
            return self._entities[entity_id]
        except KeyError:
            raise ResourceNotFoundError

    def get_entities(self):
        return list(self._entities.values())

    def get_view(self, perceptor):
        x = perceptor.x
        y = perceptor.y
        percept = []
        entities = self.get_entities()
        for entity in entities:
            if entity != perceptor:
                entity_view = {"x":          entity.x - x,
                               "y":          entity.y - y,
                               "looks_like": entity.looks_like}
                percept.append(entity_view)

        return percept

    def step(self):
        for entity in self.get_entities():
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

    def to_dict(self):
        return {
            "steps": self.steps,
            "entities": {
                key: value.to_dict() for key, value in self._entities.items()
            }
        }


def room_from_dict(data):
    new_room = Room(data["steps"])
    for entity_id, entity in data["entities"].items():
        new_room.add_entity(entity_from_dict(entity), entity_id=entity_id)
    return new_room
