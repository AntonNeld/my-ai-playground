from typing import Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.ai import AI

LooksLike = Union[Literal["player"], Literal["coin"], Literal["wall"]]


class ScorePickup(BaseModel):
    kind: Literal["addScore"]
    score: int


Pickup = Union[ScorePickup]


class Entity(BaseModel):
    x: int
    y: int
    ai: Optional[AI]
    score: Optional[int]
    blocks_movement: bool = Field(
        None, alias="blocksMovement")
    can_pickup: Union[Literal["auto"], Literal["action"]
                      ] = Field(None, alias="canPickup")
    pickup: Optional[Pickup]
    looks_like: LooksLike = Field(None, alias="looksLike")
