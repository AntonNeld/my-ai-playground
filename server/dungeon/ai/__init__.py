from typing import Union

from .pathfinder import PathfinderAI
from .singular import SingularAI
from .random import RandomAI
from .exhaustive import ExhaustiveAI

AI = Union[SingularAI, PathfinderAI, ExhaustiveAI, RandomAI]

__all__ = ("AI",)
