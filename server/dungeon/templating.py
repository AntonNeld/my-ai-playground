import json
import yaml
from pathlib import Path
import re
from typing import List, Dict, Union
import uuid

from pydantic import BaseModel

from errors import ResourceNotFoundError
from dungeon.entity import Entity, Position
from dungeon.room import Room


class Template(BaseModel):
    entities: List[Entity]

    def create_room(self):
        new_room = Room()
        for entity in self.entities:
            new_room.add_entity(entity.copy(deep=True))
        return new_room


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

    def load_directory(self, directory):
        parent_dir = Path(directory)
        for p in parent_dir.glob("./*.json"):
            with p.open() as f:
                template = Template(**json.load(f))
                self.add_template(template, template_id=p.stem)
        for p in parent_dir.glob("./*.yaml"):
            with p.open() as f:
                template = Template(**yaml.safe_load(f))
                self.add_template(template, template_id=p.stem)
        for p in parent_dir.glob("./*.txt"):
            with p.open() as f:
                template = template_from_txt(f.read())
                self.add_template(template, template_id=p.stem)


class ParseError(Exception):
    pass


class TextTemplateHeader(BaseModel):
    definitions: Dict[str, Union[Entity, str, List[Union[Entity, str]]]] = {}


def template_from_txt(txt):
    """
    Create a template from a string of the following format:

    The string begins with a header defining the symbols and global
    room parameters. The header is a JSON-encoded object following
    TextTemplateHeader. The definitions property is a mapping from
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
    header = TextTemplateHeader(**json.loads(header_no_comments))
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
    return Template(entities=entities)
