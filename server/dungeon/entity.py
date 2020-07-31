from typing import Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.ai import AI

LooksLike = Union[Literal["player"], Literal["coin"], Literal["wall"],
                  Literal["vacuum"], Literal["dirt"], Literal["labelA"],
                  Literal["labelB"]]


class Position(BaseModel):
    x: int
    y: int


class ScorePickup(BaseModel):
    kind: Literal["addScore"]
    score: int


Pickup = Union[ScorePickup]


class Perception(BaseModel):
    distance: Optional[int]


class Entity(BaseModel):
    position: Optional[Position]
    ai: Optional[AI]
    perception: Optional[Perception]
    score: Optional[int]
    blocks_movement: Optional[Literal[True]] = Field(
        None, alias="blocksMovement")
    can_pickup: Optional[Union[Literal["auto"], Literal["action"]
                               ]] = Field(None, alias="canPickup")
    pickup: Optional[Pickup]
    looks_like: Optional[LooksLike] = Field(None, alias="looksLike")
