from typing import Dict, List, Optional, Union

from typing_extensions import Literal
from pydantic import BaseModel


LooksLike = Union[Literal["player"], Literal["coin"], Literal["wall"]]
CollisionBehavior = Union[Literal["block"], Literal["vanish"]]


class Entity(BaseModel):
    x: int
    y: int
    ai: Optional[str]
    score: Optional[int]
    collisionBehavior: Optional[CollisionBehavior]
    scoreOnDestroy: Optional[int]
    looksLike: LooksLike


class Room(BaseModel):
    steps: int
    entities: Dict[str, Entity]


class Template(BaseModel):
    entities: List[Entity]
