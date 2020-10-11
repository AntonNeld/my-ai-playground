import uuid
from typing import Dict, List

from pydantic import BaseModel

from errors import ResourceNotFoundError
from dungeon.entity import (
    Entity, Position, Perception, Scoring, Vulnerable, CountTagsScore,
    ActionDetails, BlocksMovement, Pickup, Pickupper, LooksLike,
)
from dungeon.ai import AI
from profiling import time_profiling, memory_profiling
from .consts import DoNothing
from dungeon.position_dict import PositionDict
from dungeon.systems import PerceptSystem

# Initialize this once instead of in each step
doNothing = DoNothing()


COMPONENTS = {
    "position",
    "ai",
    "perception",
    "score",
    "scoring",
    "blocks_movement",
    "pickupper",
    "pickup",
    "looks_like",
    "tags",
    "label",
    "vulnerable",
    "count_tags_score",
    "actions"
}


class Room(BaseModel):
    steps: int = 0
    # Private fields
    entity_ids: List[str] = []
    # Components, also private
    position: Dict[str, Position] = PositionDict()
    ai: Dict[str, AI] = {}
    perception: Dict[str, Perception] = {}
    score: Dict[str, int] = {}
    scoring: Dict[str, Scoring] = {}
    blocks_movement: Dict[str, BlocksMovement] = {}
    pickupper: Dict[str, Pickupper] = {}
    pickup: Dict[str, Pickup] = {}
    looks_like: Dict[str, LooksLike] = {}
    tags: Dict[str, List[str]] = {}
    label: Dict[str, str] = {}
    vulnerable: Dict[str, Vulnerable] = {}
    count_tags_score: Dict[str, CountTagsScore] = {}
    actions: Dict[str, Dict[str, ActionDetails]] = {}

    class Config:
        extra = "allow"

    def __init__(self, entities=None, **kwargs):
        super().__init__(**kwargs)
        self.percept_system = PerceptSystem()
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
        return {
            **only_public, "entities": {
                entity_id: entity for entity_id, entity
                in self.get_entities(include_id=True)
            }
        }

    def add_entity(self, entity, entity_id=None):
        if entity_id is None:
            entity_id = uuid.uuid4().hex
        # Replace the entity if it already exists
        if entity_id in self.entity_ids:
            self.remove_entity_by_id(entity_id)
        self.entity_ids.append(entity_id)
        for component_name in COMPONENTS:
            component = getattr(entity, component_name)
            if component is not None:
                getattr(self, component_name)[entity_id] = component
        return entity_id

    def remove_entity_by_id(self, entity_id):
        for component_name in COMPONENTS:
            if entity_id in getattr(self, component_name):
                del getattr(self, component_name)[entity_id]
        self.entity_ids.remove(entity_id)

    def list_entities(self):
        return self.entity_ids

    def get_entity(self, entity_id):
        if entity_id not in self.entity_ids:
            raise ResourceNotFoundError
        entity = Entity()
        for component_name in COMPONENTS:
            if entity_id in getattr(self, component_name):
                component = getattr(self, component_name)[entity_id]
                setattr(entity, component_name, component)
        return entity

    def get_entities(self, include_id=False, **kwargs):
        entities_with_id = [(entity_id, self.get_entity(entity_id))
                            for entity_id in self.entity_ids]
        filtered = list(filter(lambda e: all(getattr(e[1], key) == value
                                             for key, value in kwargs.items()),
                               entities_with_id))
        if include_id:
            return filtered
        return [e for i, e in filtered]

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
            percepts = self.percept_system.get_percepts(
                self.perception, self.position, self.looks_like,
                self.pickupper)
            for entity_id in list(self.entity_ids):
                # Skip if the entity has already been removed
                if entity_id not in self.list_entities():
                    continue
                # Only entities with a position can act
                # This is a proxy for not being picked up,
                # and should be fixed.
                if entity_id in self.position:
                    # Update AI state and find next action
                    if entity_id in self.ai:
                        try:
                            percept = percepts[entity_id]
                        except KeyError:
                            percept = {}
                        do_time_profiling = (entity_id in self.label
                                             and time_profiling.started)
                        do_memory_profiling = (entity_id in self.label
                                               and memory_profiling.started)
                        if do_time_profiling:
                            time_profiling.set_context(self.label[entity_id])
                        if do_memory_profiling:
                            memory_profiling.set_context(self.label[entity_id])
                        ai = self.ai[entity_id]
                        if hasattr(ai, "update_state_percept"):
                            ai.update_state_percept(percept)
                        action = ai.next_action(percept)
                        if hasattr(ai, "update_state_action"):
                            ai.update_state_action(action)
                        if do_time_profiling:
                            time_profiling.unset_context(self.label[entity_id])
                        if do_memory_profiling:
                            memory_profiling.unset_context(
                                self.label[entity_id])
                    else:
                        action = doNothing
                    # Don't perform actions we're not allowed to
                    if (entity_id not in self.actions
                            or action.action_type not in
                            self.actions[entity_id]):
                        action = doNothing
                    else:
                        action_type = action.action_type
                        if (self.actions[entity_id][action_type].cost
                                is not None
                                and entity_id in self.score):
                            cost = self.actions[entity_id][action_type].cost
                            self.score[entity_id] -= cost
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
                        new_x = self.position[entity_id].x + dx
                        new_y = self.position[entity_id].y + dy
                        colliding_entities = [
                            self.get_entity(e) for e in
                            self.position.get_entities_at(new_x, new_y)
                            if e is not entity_id
                        ]
                        if not any(
                            map(
                                lambda e: e.blocks_movement is not None
                                and not set(
                                    e.blocks_movement.passable_for_tags
                                ) & set(
                                    self.get_entity(entity_id).get_tags()
                                ),
                                colliding_entities)):
                            self.position[entity_id] = Position(
                                x=new_x, y=new_y)

                    # Handle colissions
                    overlapping_entities = [
                        e for e in self.position.get_entities_at(
                            self.position[entity_id].x,
                            self.position[entity_id].y
                        )
                        if e is not entity_id
                    ]
                    if entity_id in self.count_tags_score:
                        tags = {
                            tag: 0 for tag
                            in self.count_tags_score[entity_id].tags}
                        for overlapping_entity in overlapping_entities:
                            for tag in self.get_entity(
                                    overlapping_entity).get_tags():
                                if tag in tags:
                                    tags[tag] += 1
                        if tags == self.count_tags_score[entity_id].tags:
                            add_to_id, add_to = self.get_entities(
                                include_id=True,
                                label=self.count_tags_score[entity_id].add_to
                            )[0]
                            if add_to.score is not None:
                                score = self.count_tags_score[entity_id].score
                                self.score[add_to_id] += score
                    if (entity_id in self.pickupper
                            and (self.pickupper[entity_id].mode == "auto"
                                 or action.action_type == "pick_up")):
                        pickups = [
                            (e, self.get_entity(e)) for e
                            in overlapping_entities
                            if self.get_entity(e).pickup is not None
                        ]
                        for pickup_id, pickup in pickups:
                            kind = pickup.pickup.kind
                            if (
                                kind == "item" and not
                                self.pickupper[entity_id].full_inventory()
                            ):
                                self.remove_entity_by_id(pickup_id)
                                pickup.position = None
                                self.pickupper[entity_id].inventory.append(
                                    pickup)
                            elif kind == "vanish":
                                self.remove_entity_by_id(pickup_id)
                            elif kind == "addScore":
                                self.remove_entity_by_id(pickup_id)
                                added_score = pickup.pickup.score
                                if entity_id in self.score:
                                    self.score[entity_id] += added_score
                    # Drop items (do this after collisions to not immediately
                    # pick them up again)
                    if action.action_type == "drop":
                        try:
                            inventory = self.pickupper[entity_id].inventory
                            dropped_entity = inventory.pop(action.index)
                            new_position = self.position[entity_id].copy(
                                deep=True)
                            dropped_entity.position = new_position
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

                        target_x = self.position[entity_id].x + dx
                        target_y = self.position[entity_id].y + dy

                        targets = [(e, self.get_entity(
                            e)) for e in self.position.get_entities_at(
                                target_x, target_y)]
                        for target_id, target in targets:
                            if target.vulnerable is not None:
                                self.remove_entity_by_id(target_id)

            self.steps += 1
