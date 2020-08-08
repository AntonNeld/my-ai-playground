from typing import Union

from .pathfinder import PathfinderAI
from .singular import SingularAI
from .random import RandomAI
from .reflex_vacuum_agent import ReflexVacuumAgentAI
from .reflex_vacuum_with_state import ReflexVacuumWithStateAI

AI = Union[SingularAI, PathfinderAI, RandomAI,
           ReflexVacuumAgentAI, ReflexVacuumWithStateAI]

__all__ = ("AI",)
