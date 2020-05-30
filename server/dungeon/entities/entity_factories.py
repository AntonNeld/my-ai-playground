from .coin import Coin
from .player import Player
from .wall import Wall
from dungeon.ai import PathfinderAI, ManualAI, RandomAI, ExhaustiveAI


def entity_from_json(entity):
    x = entity["x"]
    y = entity["y"]
    entity_id = entity["id"] if "id" in entity else None
    score = entity["score"] if "score" in entity else None
    if entity["type"] == "block":
        return Wall(x, y, entity_id=entity_id)
    elif entity["type"] == "player":
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
        return Player(x, y, ai, entity_id=entity_id, score=score)
    elif entity["type"] == "coin":
        return Coin(x, y, entity_id=entity_id)