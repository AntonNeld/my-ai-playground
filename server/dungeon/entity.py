from __future__ import annotations
from typing import Optional, Union, List, Dict

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.ai import AI
from dungeon.scoring import Scoring

LooksLike = Union[Literal["player"], Literal["coin"], Literal["wall"],
                  Literal["vacuum"], Literal["dirt"], Literal["labelA"],
                  Literal["labelB"]]


class Position(BaseModel):
    x: int
    y: int


class ScorePickup(BaseModel):
    kind: Literal["addScore"]
    score: int


class ItemPickup(BaseModel):
    kind: Literal["item"]


class VanishPickup(BaseModel):
    kind: Literal["vanish"]


Pickup = Union[ItemPickup, ScorePickup, VanishPickup]


class Pickupper(BaseModel):
    mode: Union[Literal["auto"], Literal["action"]] = "auto"
    inventory: List[Entity] = []


class Perception(BaseModel):
    distance: Optional[int]


class CountTagsScore(BaseModel):
    add_to: str = Field(..., alias="addTo")
    score: int
    tags: Dict[str, int]


class Entity(BaseModel):
    position: Optional[Position]
    ai: Optional[AI]
    perception: Optional[Perception]
    score: Optional[int]
    scoring: Optional[Scoring]
    blocks_movement: Optional[Literal[True]] = Field(
        None, alias="blocksMovement")
    pickupper: Optional[Pickupper]
    pickup: Optional[Pickup]
    looks_like: Optional[LooksLike] = Field(None, alias="looksLike")
    tags: Optional[List[str]]
    label: Optional[str]
    count_tags_score: Optional[CountTagsScore] = Field(
        None, alias="countTagsScore")


Pickupper.update_forward_refs()
