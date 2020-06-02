from .entity import Entity


class Wall(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, "wall")

    def to_dict(self):
        entity = super().to_dict()
        entity["type"] = "block"
        return entity
