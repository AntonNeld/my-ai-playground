from typing import Union

from pydantic import BaseModel, Field
from typing_extensions import Literal

LooksLike = Union[Literal["player"], Literal["coin"], Literal["evilCoin"],
                  Literal["wall"], Literal["vacuum"], Literal["dirt"],
                  Literal["water"], Literal["labelA"], Literal["labelB"]]


class Position(BaseModel):
    x: int
    y: int


class Move(BaseModel):
    action_type: Literal["move"] = Field("move", alias="actionType")
    direction: Union[Literal["up"], Literal["down"],
                     Literal["left"], Literal["right"]]


class PickUp(BaseModel):
    action_type: Literal["pick_up"] = Field("pick_up", alias="actionType")


class Drop(BaseModel):
    action_type: Literal["drop"] = Field("drop", alias="actionType")
    index: int = 0


class DoNothing(BaseModel):
    action_type: Literal["none"] = Field("none", alias="actionType")


Action = Union[Move, PickUp, Drop, DoNothing]
