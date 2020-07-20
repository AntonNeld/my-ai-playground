import uuid

from errors import ResourceNotFoundError
from dungeon.entities.entity_factories import entity_from_dict


class Room:

    def __init__(self, steps):
        self._entities = {}
        self.steps = steps

    def add_entity(self, entity, entity_id=None):
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
            # Find next action
            action = entity.ai.next_move(self.get_view(
                entity)) if entity.ai is not None else "none"
            # Move and handle collisions
            dx = dy = 0

            if action == "move_up":
                dy = 1
            elif action == "move_down":
                dy = -1
            elif action == "move_left":
                dx = -1
            elif action == "move_right":
                dx = 1

            colliding_entities = [e for e in self.get_entities(
            ) if e.x == entity.x+dx and e.y == entity.y+dy and e != entity]
            if "block" not in map(lambda e: e.collision_behavior,
                                  colliding_entities):
                entity.x += dx
                entity.y += dy
                for colliding_entity in colliding_entities:
                    if colliding_entity.collision_behavior == "vanish":
                        self.remove_entity(colliding_entity)
                        if colliding_entity.score_on_destroy is not None:
                            if entity.score is None:
                                entity.score = 0
                            entity.score += colliding_entity.score_on_destroy

        self.steps += 1

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
