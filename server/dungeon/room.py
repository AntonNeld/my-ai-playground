import uuid
from typing import Dict, Tuple

from pydantic import BaseModel

from errors import ResourceNotFoundError
from dungeon.entity import Entity, Position
from profiling import time_profiling, memory_profiling
from .consts import DoNothing

# Initialize this once instead of in each step
doNothing = DoNothing()


class Room(BaseModel):
    steps: int = 0
    # Private fields
    private_entities: Dict[str, Entity] = {}
    entities_by_location: Dict[Tuple[int, int], str] = {}

    def __init__(self, entities=None, **kwargs):
        super().__init__(**kwargs)
        if entities is not None:
            for identifier, entity in entities.items():
                entity_obj = entity if isinstance(
                    entity, Entity) else Entity(**entity)
                self.add_entity(entity_obj, entity_id=identifier)

    def dict(self, include=None, **kwargs):
        public_fields = {"steps"}
        new_include = (include | public_fields if include is not None
                       else public_fields)
        only_public = super().dict(**{"include": new_include, **kwargs})
        return {**only_public, "entities": self.private_entities}

    def add_entity(self, entity, entity_id=None):
        if entity_id is None:
            entity_id = uuid.uuid4().hex
        # Replace the entity if it already exists
        if entity_id in self.private_entities:
            self.remove_entity_by_id(entity_id)
        self.private_entities[entity_id] = entity
        if entity.position is not None:
            x = entity.position.x
            y = entity.position.y
            self._add_entity_to_locations(entity_id, x, y)
        return entity_id

    def remove_entity(self, entity):
        id_to_remove = None
        for entity_id, entity_object in self.private_entities.items():
            if entity_object == entity:
                id_to_remove = entity_id
        self.remove_entity_by_id(id_to_remove)

    def remove_entity_by_id(self, entity_id):
        if entity_id in self.private_entities:
            entity = self.private_entities[entity_id]
            if (entity.position is not None):
                x = entity.position.x
                y = entity.position.y
                self._remove_entity_from_locations(entity_id, x, y)

            del self.private_entities[entity_id]

    def _add_entity_to_locations(self, entity_id, x, y):
        if (x, y) not in self.entities_by_location:
            self.entities_by_location[(x, y)] = []
        self.entities_by_location[(x, y)].append(entity_id)

    def _remove_entity_from_locations(self, entity_id, x, y):
        self.entities_by_location[(x, y)].remove(entity_id)
        if len(self.entities_by_location[(x, y)]) == 0:
            del self.entities_by_location[(x, y)]

    def move_entity(self, entity_id, entity, x, y):
        old_x = entity.position.x
        old_y = entity.position.y
        self._remove_entity_from_locations(entity_id, old_x, old_y)
        entity.position = Position(x=x, y=y)
        self._add_entity_to_locations(entity_id, x, y)

    def list_entities(self):
        return list(self.private_entities.keys())

    def get_entity(self, entity_id):
        try:
            return self.private_entities[entity_id]
        except KeyError:
            raise ResourceNotFoundError

    def get_entities(self, include_id=False, **kwargs):
        with_id = list(filter(lambda e: all(getattr(e[1], key) == value
                                            for key, value in kwargs.items()),
                              self.private_entities.items()))
        if include_id:
            return with_id
        return [e for i, e in with_id]

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
        if perceptor.pickupper is not None:
            percept["inventory"] = [
                e.looks_like for e in perceptor.pickupper.inventory
            ]
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
            for entity_id, entity in self.get_entities(include_id=True):
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
                        action = entity.ai.next_action(percept)
                        if hasattr(entity.ai, "update_state_action"):
                            entity.ai.update_state_action(action)
                        if do_time_profiling:
                            time_profiling.unset_context(entity.label)
                        if do_memory_profiling:
                            memory_profiling.unset_context(entity.label)
                    else:
                        action = doNothing
                    # Don't perform actions we're not allowed to
                    if (entity.actions is None
                            or action.action_type not in entity.actions):
                        action = doNothing
                    else:
                        action_type = action.action_type
                        if (entity.actions[action_type].cost is not None
                                and entity.score is not None):
                            entity.score -= entity.actions[action_type].cost

                    # Move
                    dx = dy = 0

                    if action.action_type == "move":
                        if action.direction == "up":
                            dy = 1
                        elif action.direction == "down":
                            dy = -1
                        elif action.direction == "left":
                            dx = -1
                        elif action.direction == "right":
                            dx = 1

                    if dx != 0 or dy != 0:
                        new_x = entity.position.x + dx
                        new_y = entity.position.y + dy
                        colliding_entities = [
                            self.get_entity(e) for e in
                            self.get_entities_at(new_x, new_y)
                            if e is not entity_id
                        ]
                        if not any(map(lambda e: e.blocks_movement is not None
                                       and not set(entity.get_tags()) & set(
                                           e.blocks_movement.passable_for_tags
                                       ),
                                       colliding_entities)):
                            self.move_entity(entity_id, entity, new_x, new_y)

                    # Handle colissions
                    overlapping_entities = [
                        self.get_entity(e) for e
                        in self.get_entities_at(entity.position.x,
                                                entity.position.y)
                        if e is not entity_id
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
                                 or action.action_type == "pick_up")):
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
                    # Drop items (do this after collisions to not immediately
                    # pick them up again)
                    if action.action_type == "drop":
                        try:
                            dropped_entity = entity.pickupper.inventory.pop(
                                action.index)
                            dropped_entity.position = entity.position.copy(
                                deep=True)
                            self.add_entity(dropped_entity)
                        except IndexError:
                            pass
                    if action.action_type == "attack":
                        dx = dy = 0
                        if action.direction == "up":
                            dy = 1
                        elif action.direction == "down":
                            dy = -1
                        elif action.direction == "left":
                            dx = -1
                        elif action.direction == "right":
                            dx = 1

                        target_x = entity.position.x + dx
                        target_y = entity.position.y + dy

                        targets = [self.get_entity(
                            e) for e in self.get_entities_at(
                                target_x, target_y)]
                        for target in targets:
                            if target.vulnerable is not None:
                                self.remove_entity(target)

            self.steps += 1
