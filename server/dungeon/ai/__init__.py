from typing import Union

from .pathfinder import PathfinderAI
from .singular import SingularAI
from .random import RandomAI
from .reflex_vacuum_agent import ReflexVacuumAgentAI

AI = Union[SingularAI, PathfinderAI, RandomAI, ReflexVacuumAgentAI]

__all__ = ("AI",)
