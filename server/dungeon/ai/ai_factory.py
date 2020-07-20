from .pathfinder import PathfinderAI
from .manual import ManualAI
from .random import RandomAI
from .exhaustive import ExhaustiveAI


def ai_from_dict(ai):  # Not a dict yet
    if ai == "manual":
        return ManualAI()
    elif ai == "pathfinder":
        return PathfinderAI()
    elif ai == "exhaustive":
        return ExhaustiveAI()
    elif ai == "random":
        return RandomAI()
    else:
        raise RuntimeError(f"Unknown ai {ai}")
