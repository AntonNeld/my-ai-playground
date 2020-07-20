from .entity import Entity
from dungeon.ai import ai_from_dict


def entity_from_dict(entity):
    if "ai" not in entity:
        ai = None
    else:
        ai = ai_from_dict(entity["ai"])
    return Entity(ai=ai, **{key: value for key, value in entity.items()
                            if key != "ai"})
