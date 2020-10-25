from __future__ import annotations
from typing import Optional, Union, List, Dict

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.ai import AI
from dungeon.consts import LooksLike, Position


class ScorePickup(BaseModel):
    kind: Literal["addScore"]
    score: int


class ItemPickup(BaseModel):
    kind: Literal["item"]
    provides_tags: List[str] = Field([], alias="providesTags")


class VanishPickup(BaseModel):
    kind: Literal["vanish"]


Pickup = Union[ItemPickup, ScorePickup, VanishPickup]


class Pickupper(BaseModel):
    mode: Union[Literal["auto"], Literal["action"]] = "auto"
    inventory: List[Entity] = []
    inventory_limit: Optional[int] = Field(None, alias="inventoryLimit")


class Perception(BaseModel):
    distance: Optional[int]
    include_position: bool = Field(False, alias="includePosition")


class CountTagsScore(BaseModel):
    add_to: str = Field(..., alias="addTo")
    score_type: Union[Literal["constant"],
                      Literal["additive"]] = Field(..., alias="scoreType")
    score: int
    tags: Dict[str, int]


class ActionDetails(BaseModel):
    cost: Optional[int]


class BlocksMovement(BaseModel):
    passable_for_tags: List[str] = Field([], alias="passableForTags")


class Vulnerable(BaseModel):
    pass


class Entity(BaseModel):
    position: Optional[Position]
    ai: Optional[AI]
    perception: Optional[Perception]
    score: Optional[int]
    blocks_movement: Optional[BlocksMovement] = Field(
        None, alias="blocksMovement")
    pickupper: Optional[Pickupper]
    pickup: Optional[Pickup]
    looks_like: Optional[LooksLike] = Field(None, alias="looksLike")
    tags: Optional[List[str]]
    label: Optional[str]
    vulnerable: Optional[Vulnerable]
    count_tags_score: Optional[CountTagsScore] = Field(
        None, alias="countTagsScore")
    actions: Optional[Dict[str, ActionDetails]]


Pickupper.update_forward_refs()
