from typing import Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.ai import AI

LooksLike = Union[Literal["player"], Literal["coin"], Literal["wall"]]
CollisionBehavior = Union[Literal["block"], Literal["vanish"]]


class Entity(BaseModel):
    x: int
    y: int
    ai: Optional[AI]
    score: Optional[int]
    collision_behavior: Optional[CollisionBehavior] = Field(
        None, alias="collisionBehavior")
    score_on_destroy: Optional[int] = Field(None, alias="scoreOnDestroy")
    looks_like: LooksLike = Field(None, alias="looksLike")
