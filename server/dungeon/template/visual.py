from typing_extensions import Literal
from pydantic import BaseModel, Field

from dungeon.entity import Position
from dungeon.room import Room
from .common import Definitions, translate_definition_symbol


class VisualTemplate(BaseModel):
    template_type: Literal["visual"] = Field(..., alias="templateType")
    definitions: Definitions
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
                    for entity in translate_definition_symbol(
                        symbol,
                        self.definitions
                    ):
                        new_entity = entity.copy(deep=True)
                        new_entity.position = Position(
                            x=x, y=len(lines) - y - 1)
                        new_room.add_entity(new_entity)
        return new_room
