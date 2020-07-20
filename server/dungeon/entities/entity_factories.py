from .entity import Entity
from dungeon.ai import PathfinderAI, ManualAI, RandomAI, ExhaustiveAI


def entity_from_dict(entity):
    if "ai" not in entity:
        ai = None
    elif entity["ai"] == "pathfinder":
        ai = PathfinderAI()
    elif entity["ai"] == "manual":
        ai = ManualAI()
    elif entity["ai"] == "random":
        ai = RandomAI()
    elif entity["ai"] == "exhaustive":
        ai = ExhaustiveAI()
    else:
        raise RuntimeError(f"Unknown AI {entity['ai']}")
    return Entity(ai=ai, **{key: value for key, value in entity.items()
                            if key != "ai"})
