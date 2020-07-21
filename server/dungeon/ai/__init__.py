from typing import Union

from .pathfinder import PathfinderAI
from .manual import ManualAI
from .random import RandomAI
from .exhaustive import ExhaustiveAI

AI = Union[ManualAI, PathfinderAI, ExhaustiveAI, RandomAI]

__all__ = ("AI",)
