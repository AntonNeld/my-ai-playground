from typing import List

from typing_extensions import Literal
from pydantic import BaseModel, Field

from dungeon.entity import Entity
from dungeon.room import Room


class RawTemplate(BaseModel):
    template_type: Literal["raw"] = Field(..., alias="templateType")
    entities: List[Entity]

    def create_room(self):
        new_room = Room()
        for entity in self.entities:
            new_room.add_entity(entity.copy(deep=True))
        return new_room
