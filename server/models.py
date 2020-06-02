from typing import Dict, List, Union

from typing_extensions import Literal
from pydantic import BaseModel


class Player(BaseModel):
    x: int
    y: int
    type: Literal["player"]
    ai: str
    score: int


class PlayerTemplate(BaseModel):
    x: int
    y: int
    type: Literal["player"]
    ai: str


class Wall(BaseModel):
    x: int
    y: int
    type: Literal["block"]


class Coin(BaseModel):
    x: int
    y: int
    type: Literal["coin"]


Entity = Union[Player, Wall, Coin]
EntityTemplate = Union[PlayerTemplate, Wall, Coin]


class Room(BaseModel):
    steps: int
    entities: Dict[str, Entity]


class Template(BaseModel):
    entities: List[EntityTemplate]
