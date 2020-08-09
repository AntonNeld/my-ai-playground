from typing import Union

from .pathfinder import PathfinderAI
from .singular import SingularAI
from .random import RandomAI
from .reflex_vacuum_agent import ReflexVacuumAgentAI
from .reflex_vacuum_with_state import ReflexVacuumWithStateAI
from .reflex_vacuum_see_all import ReflexVacuumSeeAllAI
from .random_vacuum import RandomVacuumAI

AI = Union[SingularAI, PathfinderAI, RandomAI, ReflexVacuumAgentAI,
           ReflexVacuumWithStateAI, ReflexVacuumSeeAllAI, RandomVacuumAI]

__all__ = ("AI",)
