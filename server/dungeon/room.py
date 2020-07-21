import uuid
from typing import Dict

from pydantic import BaseModel

from errors import ResourceNotFoundError
from dungeon.entities.entity import Entity


class Room(BaseModel):
    steps: int
    entities: Dict[str, Entity]

    def add_entity(self, entity, entity_id=None):
        if entity_id is None:
            entity_id = uuid.uuid4().hex
        self.entities[entity_id] = entity
        return entity_id

    def remove_entity(self, entity):
        id_to_remove = None
        for entity_id, entity_object in self.entities.items():
            if entity_object == entity:
                id_to_remove = entity_id
        del self.entities[id_to_remove]

    def remove_entity_by_id(self, entity_id):
        if entity_id in self.entities:
            del self.entities[entity_id]

    def list_entities(self):
        return list(self.entities.keys())

    def get_entity(self, entity_id):
        try:
            return self.entities[entity_id]
        except KeyError:
            raise ResourceNotFoundError

    def get_entities(self):
        return list(self.entities.values())

    def get_view(self, perceptor):
        x = perceptor.x
        y = perceptor.y
        percept = []
        entities = self.get_entities()
        for entity in entities:
            if entity != perceptor:
                entity_view = {"x":          entity.x - x,
                               "y":          entity.y - y,
                               "looks_like": entity.looksLike}
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
            if "block" not in map(lambda e: e.collisionBehavior,
                                  colliding_entities):
                entity.x += dx
                entity.y += dy
                for colliding_entity in colliding_entities:
                    if colliding_entity.collisionBehavior == "vanish":
                        self.remove_entity(colliding_entity)
                        if colliding_entity.scoreOnDestroy is not None:
                            if entity.score is None:
                                entity.score = 0
                            entity.score += colliding_entity.scoreOnDestroy

        self.steps += 1
