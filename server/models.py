from typing import Dict, List, Union

from typing_extensions import Literal
from pydantic import BaseModel


LooksLike = Union[Literal["player"], Literal["coin"], Literal["wall"]]


class Player(BaseModel):
    x: int
    y: int
    type: Literal["player"]
    ai: str
    score: int
    solid: bool
    looksLike: LooksLike


class PlayerTemplate(BaseModel):
    x: int
    y: int
    type: Literal["player"]
    ai: str
    solid: bool
    looksLike: LooksLike


class Wall(BaseModel):
    x: int
    y: int
    type: Literal["block"]
    solid: bool
    looksLike: LooksLike


class Coin(BaseModel):
    x: int
    y: int
    type: Literal["coin"]
    solid: bool
    looksLike: LooksLike


Entity = Union[Player, Wall, Coin]
EntityTemplate = Union[PlayerTemplate, Wall, Coin]


class Room(BaseModel):
    steps: int
    entities: Dict[str, Entity]


class Template(BaseModel):
    entities: List[EntityTemplate]
