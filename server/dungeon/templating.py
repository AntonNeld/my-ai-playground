import json
from pathlib import Path
import re
from typing import List
import uuid

from pydantic import BaseModel

from errors import ResourceNotFoundError
from dungeon.entity import Entity
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
    after a newline:
    <symbol>=<definition>

    A line that does not follow this format (and is not in the middle of a
    JSON string) is ignored and can be used for comments.

    A symbol is one unicode character, a definition is usually a JSON-encoded
    object defining an entity. The definition can be split up across
    multiple lines, but cannot have empty lines in it. A definition
    can also be a JSON-encoded array of entities and/or other
    symbols, which means there are multiple entities in the same location.
    It can also be a symbol, if you for some reason want to have multiple
    symbols representing identical entities.

    Between the header and the body is an empty line, then the
    layout of the room is defined, with a symbol's location
    defining its entity's coordinates. 0,0 is to the lower left.
    """
    header = txt.strip().split("\n\n", 1)[0]
    definitions = {}
    current_symbol = None
    current_json = None
    for line in header.split("\n"):
        if current_symbol is None:
            without_whitespace = re.sub(r"\s+", "", line)
            if without_whitespace[1] != "=":
                continue
            current_symbol = without_whitespace[0]
            current_json = without_whitespace[2:]
        else:
            # Include a space in case the whitespace makes a difference
            current_json += " " + line
        try:
            definitions[current_symbol] = json.loads(current_json)
            current_symbol = None
            current_json = None
        except json.decoder.JSONDecodeError:
            pass
    # Should be nothing left
    if current_symbol is not None or current_json is not None:
        raise ParseError(f"Malformed header:\n{header}")
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
                    entities.append({"position": {"x": x,
                                                  "y": len(lines) - y - 1},
                                     **entity})
            else:
                raise ParseError(f"Unknown symbol: {symbol}")
    return Template(entities=entities)
