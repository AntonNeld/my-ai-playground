from typing import Union

from .cannibal import CannibalAI
from .get_nearest_coin import GetNearestCoinAI
from .missionaries_and_cannibals import MissionariesAndCannibalsAI
from .singular import SingularAI
from .random import RandomAI
from .reflex_vacuum_agent import ReflexVacuumAgentAI
from .reflex_vacuum_with_state import ReflexVacuumWithStateAI
from .reflex_vacuum_see_all import ReflexVacuumSeeAllAI
from .random_vacuum import RandomVacuumAI
from .exploring_vacuum import ExploringVacuumAI
from .pathfinder import PathfinderAI
from .n_puzzle import NPuzzleAI

AI = Union[SingularAI, GetNearestCoinAI, RandomAI, ReflexVacuumAgentAI,
           ReflexVacuumWithStateAI, ReflexVacuumSeeAllAI, RandomVacuumAI,
           MissionariesAndCannibalsAI, CannibalAI, ExploringVacuumAI,
           PathfinderAI, NPuzzleAI]

__all__ = ("AI",)
