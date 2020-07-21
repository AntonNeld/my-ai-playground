from .pathfinder import PathfinderAI
from .manual import ManualAI
from .random import RandomAI
from .exhaustive import ExhaustiveAI


def ai_from_dict(ai):
    if ai["kind"] == "manual":
        return ManualAI(ai["plan"] if "plan" in ai else None)
    elif ai["kind"] == "pathfinder":
        return PathfinderAI(ai["plan"] if "plan" in ai else None)
    elif ai["kind"] == "exhaustive":
        return ExhaustiveAI(ai["plan"] if "plan" in ai else None)
    elif ai["kind"] == "random":
        return RandomAI()
    else:
        raise RuntimeError(f"Unknown ai {ai}")
