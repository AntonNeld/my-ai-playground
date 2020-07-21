from .entity import Entity


def entity_from_dict(entity):
    return Entity(**entity)
