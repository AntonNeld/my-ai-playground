from typing import List, Optional

from typing_extensions import Literal
from pydantic import BaseModel, Field

from dungeon.entity import Entity
from dungeon.room import Room


class RawTemplate(BaseModel):
    template_type: Literal["raw"] = Field(..., alias="templateType")
    random_seed: Optional[int] = Field(None, alias="randomSeed")
    entities: List[Entity]

    def create_room(self):
        if self.random_seed is not None:
            new_room = Room(randomSeed=self.random_seed)
        else:
            new_room = Room()
        for entity in self.entities:
            new_room.add_entity(entity.copy(deep=True))
        return new_room
