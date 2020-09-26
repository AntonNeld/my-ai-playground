from typing import Union

from .get_nearest_coin import GetNearestCoinAI
from .singular import SingularAI
from .random import RandomAI
from .reflex_vacuum_agent import ReflexVacuumAgentAI
from .reflex_vacuum_with_state import ReflexVacuumWithStateAI
from .reflex_vacuum_see_all import ReflexVacuumSeeAllAI
from .random_vacuum import RandomVacuumAI
from .exploring_vacuum import ExploringVacuumAI
from .pathfinder import PathfinderAI

AI = Union[SingularAI, GetNearestCoinAI, RandomAI, ReflexVacuumAgentAI,
           ReflexVacuumWithStateAI, ReflexVacuumSeeAllAI, RandomVacuumAI,
           ExploringVacuumAI, PathfinderAI]

__all__ = ("AI",)
