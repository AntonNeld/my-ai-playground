from typing import Optional, Union

from pydantic import BaseModel
from typing_extensions import Literal

from dungeon.ai import AI

LooksLike = Union[Literal["player"], Literal["coin"], Literal["wall"]]
CollisionBehavior = Union[Literal["block"], Literal["vanish"]]


class Entity(BaseModel):
    x: int
    y: int
    ai: Optional[AI]
    score: Optional[int]
    collisionBehavior: Optional[CollisionBehavior]
    scoreOnDestroy: Optional[int]
    looksLike: LooksLike
