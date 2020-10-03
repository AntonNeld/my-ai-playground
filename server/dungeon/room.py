import uuid
from typing import Dict, Tuple

from pydantic import BaseModel

from errors import ResourceNotFoundError
from dungeon.entity import Entity, Position
from profiling import time_profiling, memory_profiling


class Room(BaseModel):
    steps: int = 0
    entities: Dict[str, Entity] = {}
    # Private fields
    entities_by_location: Dict[Tuple[int, int], Entity] = {}

    def dict(self, exclude=None, **kwargs):
        private_fields = {'entities_by_location'}
        new_exclude = (exclude | private_fields if exclude is not None
                       else private_fields)
        return super().dict(**{'exclude': new_exclude, **kwargs})

    def add_entity(self, entity, entity_id=None):
        if entity_id is None:
            entity_id = uuid.uuid4().hex
        # Replace the entity if it already exists
        if entity_id in self.entities:
            self.remove_entity_by_id(entity_id)
        self.entities[entity_id] = entity
        if entity.position is not None:
            x = entity.position.x
            y = entity.position.y
            self._add_entity_to_locations(entity, x, y)
        return entity_id

    def remove_entity(self, entity):
        id_to_remove = None
        for entity_id, entity_object in self.entities.items():
            if entity_object == entity:
                id_to_remove = entity_id
        self.remove_entity_by_id(id_to_remove)

    def remove_entity_by_id(self, entity_id):
        if entity_id in self.entities:
            entity = self.entities[entity_id]
            if (entity.position is not None):
                x = entity.position.x
                y = entity.position.y
                self._remove_entity_from_locations(entity, x, y)

            del self.entities[entity_id]

    def _add_entity_to_locations(self, entity, x, y):
        if (x, y) not in self.entities_by_location:
            self.entities_by_location[(x, y)] = []
        self.entities_by_location[(x, y)].append(entity)

    def _remove_entity_from_locations(self, entity, x, y):
        self.entities_by_location[(x, y)].remove(entity)
        if len(self.entities_by_location[(x, y)]) == 0:
            del self.entities_by_location[(x, y)]

    def move_entity(self, entity, x, y):
        old_x = entity.position.x
        old_y = entity.position.y
        self._remove_entity_from_locations(entity, old_x, old_y)
        entity.position = Position(x=x, y=y)
        self._add_entity_to_locations(entity, x, y)

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

    def get_entities_at(self, x, y):
        if (x, y) in self.entities_by_location:
            return self.entities_by_location[(x, y)]
        return []

    def get_view(self, perceptor):
        if perceptor.perception is None or perceptor.position is None:
            return {}

        percept = {}
        my_x = perceptor.position.x
        my_y = perceptor.position.y
        entities_view = []
        entities = self.get_entities()
        for entity in [e for e in entities if e.position is not None]:
            if entity is perceptor:
                continue
            other_x = entity.position.x
            other_y = entity.position.y
            max_dist = perceptor.perception.distance
            if (max_dist is not None
                    and abs(other_x-my_x) + abs(other_y-my_y) > max_dist):
                continue
            entity_view = {"x":          other_x - my_x,
                           "y":          other_y - my_y,
                           "looks_like": entity.looks_like}
            entities_view.append(entity_view)
        percept["entities"] = entities_view

        if perceptor.perception.include_position:
            percept["position"] = {
                "x": perceptor.position.x, "y": perceptor.position.y}
        return percept

    def get_entity_score(self, entity):
        if isinstance(entity, str):
            entity = self.get_entity(entity)
        if entity.scoring is None and entity.score is None:
            return None
        evaluated_score = (entity.scoring.get_score(
            entity, self) if entity.scoring is not None else 0)
        accumulated_score = entity.score if entity.score is not None else 0
        return evaluated_score + accumulated_score

    def step(self, steps=1):
        for _ in range(steps):
            for entity in self.get_entities():
                # Only entities with a position can act
                # This is a proxy for not being picked up,
                # and should be fixed.
                if entity.position is not None:
                    # Update AI state and find next action
                    if entity.ai is not None:
                        percept = self.get_view(entity)
                        do_time_profiling = (entity.label is not None
                                             and time_profiling.started)
                        do_memory_profiling = (entity.label is not None
                                               and memory_profiling.started)
                        if do_time_profiling:
                            time_profiling.set_context(entity.label)
                        if do_memory_profiling:
                            memory_profiling.set_context(entity.label)
                        if hasattr(entity.ai, "update_state_percept"):
                            entity.ai.update_state_percept(percept)
                        action = entity.ai.next_move(percept)
                        if hasattr(entity.ai, "update_state_action"):
                            entity.ai.update_state_action(action)
                        if do_time_profiling:
                            time_profiling.unset_context(entity.label)
                        if do_memory_profiling:
                            memory_profiling.unset_context(entity.label)
                    else:
                        action = "none"
                    # Don't perform actions we're not allowed to
                    if entity.actions is None or action not in entity.actions:
                        action = "none"
                    else:
                        if (entity.actions[action].cost is not None
                                and entity.score is not None):
                            entity.score -= entity.actions[action].cost

                    # Move
                    dx = dy = 0

                    if action == "move_up":
                        dy = 1
                    elif action == "move_down":
                        dy = -1
                    elif action == "move_left":
                        dx = -1
                    elif action == "move_right":
                        dx = 1

                    if dx != 0 or dy != 0:
                        new_x = entity.position.x + dx
                        new_y = entity.position.y + dy
                        colliding_entities = [
                            e for e in self.get_entities_at(new_x, new_y)
                            if e is not entity
                        ]
                        if not any(map(lambda e: e.blocks_movement is not None
                                       and not set(entity.get_tags()) & set(
                                           e.blocks_movement.passable_for_tags
                                       ),
                                       colliding_entities)):
                            self.move_entity(entity, new_x, new_y)

                    # Handle colissions
                    overlapping_entities = [
                        e for e in self.get_entities_at(entity.position.x,
                                                        entity.position.y)
                        if e is not entity
                    ]
                    if entity.count_tags_score is not None:
                        tags = {
                            tag: 0 for tag in entity.count_tags_score.tags}
                        for overlapping_entity in overlapping_entities:
                            for tag in overlapping_entity.get_tags():
                                if tag in tags:
                                    tags[tag] += 1
                        if tags == entity.count_tags_score.tags:
                            add_to = self.get_entities(
                                label=entity.count_tags_score.add_to)[0]
                            if add_to.score is not None:
                                score = entity.count_tags_score.score
                                add_to.score += score
                    if (entity.pickupper is not None
                            and (entity.pickupper.mode == "auto"
                                 or action == "pick_up")):
                        pickups = [
                            e for e in overlapping_entities
                            if e.pickup is not None
                        ]
                        for pickup in pickups:
                            kind = pickup.pickup.kind
                            if (kind == "item"
                                    and not entity.pickupper.full_inventory()):
                                self.remove_entity(pickup)
                                pickup.position = None
                                entity.pickupper.inventory.append(
                                    pickup)
                            elif kind == "vanish":
                                self.remove_entity(pickup)
                            elif kind == "addScore":
                                self.remove_entity(pickup)
                                added_score = pickup.pickup.score
                                if entity.score is not None:
                                    entity.score += added_score
            self.steps += 1
