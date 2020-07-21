from .pathfinder import PathfinderAI
from .manual import ManualAI
from .random import RandomAI
from .exhaustive import ExhaustiveAI


def ai_from_dict(ai):
    if ai["kind"] == "manual":
        return ManualAI(**ai)
    elif ai["kind"] == "pathfinder":
        return PathfinderAI(**ai)
    elif ai["kind"] == "exhaustive":
        return ExhaustiveAI(**ai)
    elif ai["kind"] == "random":
        return RandomAI(**ai)
    else:
        raise RuntimeError(f"Unknown ai {ai['kind']}")
