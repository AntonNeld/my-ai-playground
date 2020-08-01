import uuid
from typing import Dict

from pydantic import BaseModel

from errors import ResourceNotFoundError
from dungeon.entity import Entity


class Room(BaseModel):
    steps: int = 0
    entities: Dict[str, Entity] = {}

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

    def get_entities(self, **kwargs):
        return list(filter(lambda e: all(getattr(e, key) == value
                                         for key, value in kwargs.items()),
                           self.entities.values()))

    def get_view(self, perceptor):
        if perceptor.perception is None or perceptor.position is None:
            return {}
        my_x = perceptor.position.x
        my_y = perceptor.position.y
        percept = []
        entities = self.get_entities()
        for entity in [e for e in entities if e.position is not None]:
            other_x = entity.position.x
            other_y = entity.position.y
            distance = abs(other_x-my_x) + abs(other_y-my_y)
            if entity != perceptor and (perceptor.perception.distance is None
                                        or distance
                                        <= perceptor.perception.distance):
                entity_view = {"x":          other_x - my_x,
                               "y":          other_y - my_y,
                               "looks_like": entity.looks_like}
                percept.append(entity_view)

        return percept

    def step(self, steps=1):
        for _ in range(steps):
            for entity in self.get_entities():
                # Only entities with a position can act
                # This is a proxy for not being picked up,
                # and should be fixed.
                if entity.position is None:
                    continue
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
                new_x = entity.position.x + dx
                new_y = entity.position.y + dy

                colliding_entities = [e for e in self.get_entities(
                ) if e.position is not None and e.position.x == new_x
                    and e.position.y == new_y and e != entity]

                if not any(map(lambda e: e.blocks_movement is True,
                               colliding_entities)):
                    entity.position.x = new_x
                    entity.position.y = new_y
                    if (entity.pickupper is not None
                            and (entity.pickupper.mode == "auto"
                                 or action == "pick_up")):
                        pickups = [
                            e for e in colliding_entities
                            if e.pickup is not None
                        ]
                        for colliding_entity in pickups:
                            self.remove_entity(colliding_entity)
                            if colliding_entity.pickup.kind == "item":
                                colliding_entity.position = None
                                entity.pickupper.inventory.append(
                                    colliding_entity)
                            elif colliding_entity.pickup.kind == "vanish":
                                pass

            self.steps += 1
