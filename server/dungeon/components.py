from typing import Union, List, Optional, Dict

from pydantic import BaseModel, Field
from typing_extensions import Literal

LooksLike = Union[Literal["player"], Literal["coin"], Literal["evilCoin"],
                  Literal["wall"], Literal["vacuum"], Literal["dirt"],
                  Literal["water"], Literal["grass"],
                  Literal["labelA"], Literal["labelB"]]


class Position(BaseModel):
    x: int
    y: int


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


class Inventory(BaseModel):
    items: List[str] = []
    limit: Optional[int]


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
