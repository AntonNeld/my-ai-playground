from .entity import Entity
from .player import Player
from dungeon.ai import PathfinderAI, ManualAI, RandomAI, ExhaustiveAI


def entity_from_dict(entity):
    x = entity["x"]
    y = entity["y"]
    if "ai" in entity:
        if entity["ai"] == "pathfinder":
            ai = PathfinderAI()
        elif entity["ai"] == "manual":
            ai = ManualAI()
        elif entity["ai"] == "random":
            ai = RandomAI()
        elif entity["ai"] == "exhaustive":
            ai = ExhaustiveAI()
        else:
            raise RuntimeError(f"Unknown AI {entity['ai']}")
        score = entity["score"] if "score" in entity else None
        return Player(x, y, ai, score)
    else:
        return Entity(**entity)
