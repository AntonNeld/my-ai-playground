from typing import Dict, List, Optional, Union

from typing_extensions import Literal
from pydantic import BaseModel


LooksLike = Union[Literal["player"], Literal["coin"], Literal["wall"]]
CollisionBehavior = Union[Literal["block"], Literal["vanish"]]
Move = Union[Literal["move_up"], Literal["move_down"],
             Literal["move_left"], Literal["move_right"], Literal["none"]]


class ManualAI(BaseModel):
    kind: Literal["manual"]
    plan: Optional[Move]


class PathfinderAI(BaseModel):
    kind: Literal["pathfinder"]
    plan: Optional[List[Move]]


class ExhaustiveAI(BaseModel):
    kind: Literal["exhaustive"]
    plan: Optional[List[Move]]


class RandomAI(BaseModel):
    kind: Literal["random"]


AI = Union[ManualAI, PathfinderAI, ExhaustiveAI, RandomAI]


class Entity(BaseModel):
    x: int
    y: int
    ai: Optional[AI]
    score: Optional[int]
    collisionBehavior: Optional[CollisionBehavior]
    scoreOnDestroy: Optional[int]
    looksLike: LooksLike


class Room(BaseModel):
    steps: int
    entities: Dict[str, Entity]


class Template(BaseModel):
    entities: List[Entity]
