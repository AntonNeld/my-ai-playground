import uuid
import random

from pydantic import BaseModel, Field

from errors import ResourceNotFoundError
from dungeon.entity import Entity


from dungeon.custom_component_dicts import PositionDict, LabelDict
from dungeon.systems import (PerceptSystem, ActionSystem, TagSystem,
                             MovementSystem, PickUpSystem, DropSystem,
                             AttackSystem, CountTagsScoreSystem)


COMPONENT_PROPS = {
    "position": "position_components",
    "ai": "ai_components",
    "perception": "perception_components",
    "score": "score_components",
    "blocks_movement": "blocks_movement_components",
    "swappable": "swappable_components",
    "pickupper": "pickupper_components",
    "inventory": "inventory_components",
    "pickup": "pickup_components",
    "looks_like": "looks_like_components",
    "tags": "tags_components",
    "label": "label_components",
    "vulnerable": "vulnerable_components",
    "count_tags_score": "count_tags_score_components",
    "actions": "actions_components"
}


class Room(BaseModel):
    steps: int = 0
    random_seed: int = Field(0, alias="randomSeed")

    class Config:
        extra = "allow"

    def __init__(self, entities=None, **kwargs):
        super().__init__(**kwargs)
        # Entities
        self.entity_ids = []
        # Components
        self.position_components = PositionDict()
        self.ai_components = {}
        self.perception_components = {}
        self.score_components = {}
        self.blocks_movement_components = {}
        self.swappable_components = {}
        self.pickupper_components = {}
        self.inventory_components = {}
        self.pickup_components = {}
        self.looks_like_components = {}
        self.tags_components = {}
        self.label_components = LabelDict()
        self.vulnerable_components = {}
        self.count_tags_score_components = {}
        self.actions_components = {}
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
                entity_id: self.get_entity(entity_id).dict(**kwargs)
                for entity_id in self.list_entities()
            }
        }

    def add_entity(self, entity, entity_id=None):
        if entity_id is None:
            entity_id = uuid.uuid4().hex
        # Replace the entity if it already exists
        if entity_id in self.entity_ids:
            self.remove_entity(entity_id)
        self.entity_ids.append(entity_id)
        for component_name, component_prop in COMPONENT_PROPS.items():
            component = getattr(entity, component_name)
            if component is not None:
                getattr(self, component_prop)[entity_id] = component
        return entity_id

    def remove_entity(self, entity_id):
        for component_prop in COMPONENT_PROPS.values():
            if entity_id in getattr(self, component_prop):
                del getattr(self, component_prop)[entity_id]
        self.entity_ids.remove(entity_id)

    def list_entities(self):
        return self.entity_ids

    def get_entity(self, entity_id):
        if entity_id not in self.entity_ids:
            raise ResourceNotFoundError
        entity = Entity()
        for component_name, component_prop in COMPONENT_PROPS.items():
            if entity_id in getattr(self, component_prop):
                component = getattr(self, component_prop)[entity_id]
                setattr(entity, component_name, component)
        return entity

    def get_entity_scores(self):
        tags = self.tag_system.get_tags(
            self.tags_components, self.inventory_components,
            self.pickup_components)
        tag_scores = self.count_tags_score_system.get_constant_tag_scores(
            self.count_tags_score_components, self.position_components,
            tags, self.label_components)
        scores = {}
        for score_source in [tag_scores, self.score_components]:
            for entity_id, score in score_source.items():
                if entity_id not in scores:
                    scores[entity_id] = 0
                scores[entity_id] += score
        return scores

    def step(self, steps=1):
        for _ in range(steps):
            random_generator = random.Random(self.random_seed)

            initial_tags = self.tag_system.get_tags(
                self.tags_components, self.inventory_components,
                self.pickup_components)

            percepts = self.percept_system.get_percepts(
                self.perception_components, self.position_components,
                self.looks_like_components, self.inventory_components)

            actions = self.action_system.get_actions(
                self.ai_components, percepts, self.actions_components,
                self.score_components, self.label_components, random_generator)

            self.movement_system.move_entities(
                actions, self.position_components,
                self.blocks_movement_components,
                initial_tags, self.swappable_components)

            removed_entities = self.pick_up_system.pick_up_items(
                self.pickupper_components, actions, self.position_components,
                self.pickup_components, self.score_components,
                self.inventory_components)
            for removed_id in removed_entities:
                self.remove_entity(removed_id)

            self.drop_system.drop_items(
                self.inventory_components, actions, self.position_components)

            removed_entities = self.attack_system.do_attacks(
                actions, self.position_components, self.vulnerable_components)
            for removed_id in removed_entities:
                self.remove_entity(removed_id)

            final_tags = self.tag_system.get_tags(
                self.tags_components, self.inventory_components,
                self.pickup_components)

            self.count_tags_score_system.add_tag_scores(
                self.count_tags_score_components, self.position_components,
                final_tags, self.label_components, self.score_components)

            self.steps += 1
            self.random_seed = hash(random_generator.getstate())
