from __future__ import annotations
from typing import Optional, Union, List, Dict

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.ai import AI
from dungeon.scoring import Scoring
from dungeon.consts import Move, LooksLike, Position


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
    include_position: bool = Field(False, alias="includePosition")


class CountTagsScore(BaseModel):
    add_to: str = Field(..., alias="addTo")
    score: int
    tags: Dict[str, int]


class ActionDetails(BaseModel):
    cost: Optional[int]


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
    actions: Optional[Dict[Move, ActionDetails]]


Pickupper.update_forward_refs()
