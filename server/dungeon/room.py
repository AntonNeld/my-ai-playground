import uuid

from pydantic import BaseModel

from errors import ResourceNotFoundError
from dungeon.entity import Entity


from .consts import DoNothing
from dungeon.position_dict import PositionDict
from dungeon.systems import (PerceptSystem, ActionSystem, TagSystem,
                             MovementSystem, PickUpSystem, DropSystem,
                             AttackSystem, CountTagsScoreSystem)

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

    class Config:
        extra = "allow"

    def __init__(self, entities=None, **kwargs):
        super().__init__(**kwargs)
        # Entities
        self.entity_ids = []
        # Components
        self.position = PositionDict()
        self.ai = {}
        self.perception = {}
        self.score = {}
        self.scoring = {}
        self.blocks_movement = {}
        self.pickupper = {}
        self.pickup = {}
        self.looks_like = {}
        self.tags = {}
        self.label = {}
        self.vulnerable = {}
        self.count_tags_score = {}
        self.actions = {}
        # Systems
        self.percept_system = PerceptSystem()
        self.action_system = ActionSystem()
        self.tag_system = TagSystem()
        self.movement_system = MovementSystem()
        self.pick_up_system = PickUpSystem()
        self.drop_system = DropSystem()
        self.attack_system = AttackSystem()
        self.count_tags_score_system = CountTagsScoreSystem()
        if entities is not None:
            for identifier, entity in entities.items():
                entity_obj = entity if isinstance(
                    entity, Entity) else Entity(**entity)
                self.add_entity(entity_obj, entity_id=identifier)

    def dict(self, include=None, **kwargs):
        if include is None:
            include = set(self.__fields__.keys())
        only_public = super().dict(include=include, **kwargs)
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
            actions = self.action_system.get_actions(
                self.ai, percepts, self.actions, self.score, self.label)
            tags_before_moving = self.tag_system.get_tags(
                self.tags, self.pickupper)
            self.movement_system.move_entities(
                actions, self.position, self.blocks_movement,
                tags_before_moving)
            picked_up, removed = self.pick_up_system.pick_up_items(
                self.pickupper, actions, self.position, self.pickup,
                self.score)
            for pickup_id, pickupper_id in picked_up.items():
                pickup = self.get_entity(pickup_id)
                pickup.position = None
                self.pickupper[pickupper_id].inventory.append(
                    pickup)
                self.remove_entity_by_id(pickup_id)
            for removed_id in removed:
                self.remove_entity_by_id(removed_id)
            created_entities = self.drop_system.drop_items(
                self.pickupper, actions, self.position)
            for entity in created_entities:
                self.add_entity(entity)
            removed_entities = self.attack_system.do_attacks(
                actions, self.position, self.vulnerable)
            for removed_id in removed_entities:
                self.remove_entity_by_id(removed_id)
            final_tags = self.tag_system.get_tags(
                self.tags, self.pickupper)
            self.count_tags_score_system.add_tag_scores(
                self.count_tags_score, self.position, final_tags, self.label,
                self.score)

            self.steps += 1
