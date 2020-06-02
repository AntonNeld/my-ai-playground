from typing import Dict, Union

from typing_extensions import Literal
from pydantic import BaseModel


class Player(BaseModel):
    x: int
    y: int
    type: Literal["player"]
    ai: str
    score: int


class Wall(BaseModel):
    x: int
    y: int
    type: Literal["block"]


class Coin(BaseModel):
    x: int
    y: int
    type: Literal["coin"]


Entity = Union[Player, Wall, Coin]


class Room(BaseModel):
    steps: int
    entities: Dict[str, Entity]
