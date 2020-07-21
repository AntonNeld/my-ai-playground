from typing import Union

from typing_extensions import Literal

Move = Union[Literal["move_up"], Literal["move_down"],
             Literal["move_left"], Literal["move_right"], Literal["none"]]
