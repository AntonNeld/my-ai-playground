import json
import yaml
from pathlib import Path
from typing import List, Dict, Union, Any, Optional
import uuid

from typing_extensions import Literal
from pydantic import BaseModel, Field
import jsonpath_ng

from errors import ResourceNotFoundError
from dungeon.entity import Entity, Position
from dungeon.room import Room


class RawTemplate(BaseModel):
    template_type: Literal["raw"] = Field(..., alias="templateType")
    entities: List[Entity]

    def create_room(self):
        new_room = Room()
        for entity in self.entities:
            new_room.add_entity(entity.copy(deep=True))
        return new_room


class VisualTemplate(BaseModel):
    template_type: Literal["visual"] = Field(..., alias="templateType")
    definitions: Dict[str, Union[Entity, str, List[Union[Entity, str]]]]
    room: str

    def create_room(self):
        new_room = Room()
        lines = [line for line in self.room.split(
            "\n") if line and not line.isspace()]
        for y, line in enumerate(lines):
            for x, symbol in enumerate(line):
                if symbol == " ":
                    pass
                else:
                    for entity in self.translate_symbol(symbol):
                        new_entity = entity.copy(deep=True)
                        new_entity.position = Position(
                            x=x, y=len(lines) - y - 1)
                        new_room.add_entity(new_entity)
        return new_room

    def translate_symbol(self, symbol, original_symbol=None):
        if symbol == original_symbol:
            raise ParseError(f"Circular reference: {symbol}")
        if symbol not in self.definitions:
            raise ParseError(f"Unknown symbol: {symbol}")
        if isinstance(self.definitions[symbol], list):
            definition_list = self.definitions[symbol]
        else:
            definition_list = [self.definitions[symbol]]
        entities = []
        for definition in definition_list:
            if isinstance(definition, Entity):
                entities.append(definition)
            else:
                entities.extend(
                    self.translate_symbol(
                        definition,
                        (original_symbol if original_symbol is not None
                         else symbol)
                    )
                )
        return entities


Template = Union[RawTemplate, VisualTemplate]


class Challenge(BaseModel):
    variants: Optional[Dict[str, Dict[str, Any]]]
    template: Template

    def create_room(self, variant=None):
        if variant is None:
            return self.template.create_room()
        template_dict = self.template.dict(by_alias=True)
        for path, value in self.variants[variant].items():
            path_expression = jsonpath_ng.parse(path)
            template_dict = path_expression.update(template_dict, value)
        TemplateClass = self.template.__class__
        template = TemplateClass(**template_dict)
        return template.create_room()


class ChallengeKeeper:

    def __init__(self):
        self._challenges = {}

    def add_challenge(self, challenge, challenge_id=None):
        if challenge_id is None:
            challenge_id = uuid.uuid4().hex
        self._challenges[challenge_id] = challenge
        return challenge_id

    def get_challenge(self, challenge_id):
        try:
            return self._challenges[challenge_id]
        except KeyError:
            raise ResourceNotFoundError

    def remove_challenge_by_id(self, challenge_id):
        if challenge_id in self._challenges:
            del self._challenges[challenge_id]

    def list_challenges(self):
        return list(self._challenges.keys())

    def load_directory(self, directory):
        parent_dir = Path(directory)
        for p in parent_dir.glob("./*.json"):
            with p.open() as f:
                challenge = Challenge(**json.load(f))
                self.add_challenge(challenge, challenge_id=p.stem)
        for p in parent_dir.glob("./*.yaml"):
            with p.open() as f:
                challenge = Challenge(**yaml.safe_load(f))
                self.add_challenge(challenge, challenge_id=p.stem)


class ParseError(Exception):
    pass
