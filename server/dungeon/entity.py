from __future__ import annotations
from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from dungeon.ai import AI
from dungeon.components import (
    LooksLike,
    Position,
    Perception,
    BlocksMovement,
    Pickupper,
    Inventory,
    Pickup,
    Vulnerable,
    CountTagsScore,
    ActionDetails
)


class Entity(BaseModel):
    position: Optional[Position]
    ai: Optional[AI]
    perception: Optional[Perception]
    score: Optional[int]
    blocks_movement: Optional[BlocksMovement] = Field(
        None, alias="blocksMovement")
    pickupper: Optional[Pickupper]
    inventory: Optional[Inventory]
    pickup: Optional[Pickup]
    looks_like: Optional[LooksLike] = Field(None, alias="looksLike")
    tags: Optional[List[str]]
    label: Optional[str]
    vulnerable: Optional[Vulnerable]
    count_tags_score: Optional[CountTagsScore] = Field(
        None, alias="countTagsScore")
    actions: Optional[Dict[str, ActionDetails]]
