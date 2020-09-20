import json
import yaml
from pathlib import Path
import re
from typing import List, Dict, Union
import uuid

from typing_extensions import Literal
from pydantic import BaseModel, Field

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


class Challenge(BaseModel):
    template: Union[RawTemplate]

    def create_room(self):
        return self.template.create_room()


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
        for p in parent_dir.glob("./*.txt"):
            with p.open() as f:
                challenge = challenge_from_txt(f.read())
                self.add_challenge(challenge, challenge_id=p.stem)


class ParseError(Exception):
    pass


class TextChallengeHeader(BaseModel):
    definitions: Dict[str, Union[Entity, str, List[Union[Entity, str]]]] = {}


def challenge_from_txt(txt):
    """
    Create a challenge from a string of the following format:

    The string begins with a header defining the symbols and global
    room parameters. The header is a JSON-encoded object following
    TextChallengeHeader. The definitions property is a mapping from
    symbols (unicode characters) to a list of entities or other
    symbols, defining what is in a tile with the corresponding symbol.
    Instead of a list, a single entity (or symbol) is also permitted.

    Lines in the header beginning with // are comments.

    Between the header and the body is an empty line, then the
    layout of the room is defined, with a symbol's location
    defining its entity's coordinates. 0,0 is to the lower left.
    """
    # Find header
    header_string = txt.strip().split("\n\n", 1)[0]
    # Strip comments
    header_no_comments = re.sub("//.*\n", "", header_string)
    header = TextChallengeHeader(**json.loads(header_no_comments))
    definitions = header.definitions
    # Make all definitions hold lists
    for symbol in definitions:
        if not isinstance(definitions[symbol], list):
            definitions[symbol] = [definitions[symbol]]
    # Dereference symbols in definitions
    for symbol in definitions:
        while any(map(lambda e: isinstance(e, str), definitions[symbol])):
            entity = definitions[symbol].pop(0)
            if entity == symbol:
                raise ParseError(f"Circular reference: {entity}")
            if isinstance(entity, str):
                definitions[symbol].extend(definitions[entity])
            else:
                definitions[symbol].append(entity)

    entities = []
    body = txt.strip().split("\n\n", 1)[1]
    lines = [line for line in body.split("\n") if line and not line.isspace()]
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol == " ":
                pass
            elif symbol in definitions:
                for entity in definitions[symbol]:
                    new_entity = entity.copy(deep=True)
                    new_entity.position = Position(x=x, y=len(lines) - y - 1)
                    entities.append(new_entity)
            else:
                raise ParseError(f"Unknown symbol: {symbol}")
    return Challenge(**{"template": {
        "templateType": "raw",
        "entities": entities
    }})
