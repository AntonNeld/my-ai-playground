from typing import Union

from .pathfinder import PathfinderAI
from .singular import SingularAI
from .random import RandomAI

AI = Union[SingularAI, PathfinderAI, RandomAI]

__all__ = ("AI",)
