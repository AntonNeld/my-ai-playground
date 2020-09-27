from typing import List, Dict, Union

from typing_extensions import Literal
from pydantic import BaseModel, Field

from dungeon.entity import Entity, Position
from dungeon.room import Room
from .common import ParseError


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
