from typing import Union

from pydantic import BaseModel
from typing_extensions import Literal

Action = Union[Literal["move_up"], Literal["move_down"],
               Literal["move_left"], Literal["move_right"],
               Literal["pick_up"], Literal["none"]]

LooksLike = Union[Literal["player"], Literal["coin"], Literal["evilCoin"],
                  Literal["wall"], Literal["vacuum"], Literal["dirt"],
                  Literal["water"], Literal["labelA"], Literal["labelB"]]


class Position(BaseModel):
    x: int
    y: int
