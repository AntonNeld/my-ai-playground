import json
from pathlib import Path
import re
from typing import List
import uuid

from pydantic import BaseModel

from errors import ResourceNotFoundError
from dungeon.entities.entity import Entity
from dungeon.room import Room


class Template(BaseModel):
    entities: List[Entity]


class TemplateKeeper:

    def __init__(self):
        self._templates = {}

    def add_template(self, template, template_id=None):
        if template_id is None:
            template_id = uuid.uuid4().hex
        self._templates[template_id] = template
        return template_id

    def get_template(self, template_id):
        try:
            return self._templates[template_id]
        except KeyError:
            raise ResourceNotFoundError

    def remove_template_by_id(self, template_id):
        if template_id in self._templates:
            del self._templates[template_id]

    def list_templates(self):
        return list(self._templates.keys())

    def create_room(self, template_id):
        template = self.get_template(template_id)
        new_room = Room(steps=0, entities={})
        for entity in template.entities:
            new_room.add_entity(entity)
        return new_room

    def load_directory(self, directory):
        parent_dir = Path(directory)
        for p in parent_dir.glob("./*.json"):
            with p.open() as f:
                template = Template(**json.load(f))
                self.add_template(template, template_id=p.stem)
        for p in parent_dir.glob("./*.txt"):
            with p.open() as f:
                template = template_from_txt(f.read())
                self.add_template(template, template_id=p.stem)


class ParseError(Exception):
    pass


def template_from_txt(txt):
    """
    Create a template from a string of the following format:

    The string begins with a header defining the symbols, each
    on its own line:
    <symbol>=<definition>

    All whitespace except newlines are ignored in the header.
    A symbol is one unicode character, a definition is one of:
    player
    coin
    block

    Between the header and the body is an empty line, then the
    layout of the room is defined, with a symbol's location
    defining its entity's coordinates. 0,0 is to the lower left.
    """
    header = txt.strip().split("\n\n", 1)[0]
    definitions = {}
    for line in header.split("\n"):
        without_whitespace = re.sub(r"\s+", "", line)
        symbol = without_whitespace[0]
        if without_whitespace[1] != "=":
            raise ParseError(f"Malformed header:\n{header}")
        definition = without_whitespace[2:]
        definitions[symbol] = definition

    entities = []
    body = txt.strip().split("\n\n", 1)[1]
    lines = [line for line in body.split("\n") if line and not line.isspace()]
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol == " ":
                pass
            elif symbol in definitions:
                definition = definitions[symbol]
                if definition == "player":
                    entity = {"looksLike": "player",
                              "ai": {"kind": "pathfinder"}}
                elif definition == "block":
                    entity = {"collisionBehavior": "block",
                              "looksLike": "wall"}
                elif definition == "coin":
                    entity = {"collisionBehavior": "vanish",
                              "looksLike": "coin",
                              "scoreOnDestroy": 1}
                else:
                    raise ParseError(f"Unknown definition: {definition}")
                entity["x"] = x
                entity["y"] = len(lines) - y - 1
                entities.append(entity)
            else:
                raise ParseError(f"Unknown symbol: {symbol}")
    return Template(entities=entities)
