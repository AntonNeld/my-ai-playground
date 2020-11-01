from typing import Union

from pydantic import BaseModel, Field
from typing_extensions import Literal

Direction = Union[Literal["up"], Literal["down"],
                  Literal["left"], Literal["right"]]


class Move(BaseModel):
    action_type: Literal["move"] = Field("move", alias="actionType")
    direction: Direction


class Swap(BaseModel):
    action_type: Literal["swap"] = Field("swap", alias="actionType")
    direction: Direction


class PickUp(BaseModel):
    action_type: Literal["pick_up"] = Field("pick_up", alias="actionType")


class Drop(BaseModel):
    action_type: Literal["drop"] = Field("drop", alias="actionType")
    index: int = 0


class DoNothing(BaseModel):
    action_type: Literal["none"] = Field("none", alias="actionType")


class Attack(BaseModel):
    action_type: Literal["attack"] = Field("attack", alias="actionType")
    direction: Direction


Action = Union[Move, Swap, PickUp, Drop, Attack, DoNothing]
