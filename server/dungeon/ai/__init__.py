from typing import Union

from dungeon.ai.ai_factory import ai_from_dict
from .pathfinder import PathfinderAI
from .manual import ManualAI
from .random import RandomAI
from .exhaustive import ExhaustiveAI

AI = Union[ManualAI, PathfinderAI, ExhaustiveAI, RandomAI]

__all__ = ("ai_from_dict", "AI")
