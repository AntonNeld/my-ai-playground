from .entity import Entity


class Coin(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, "coin", False)

    def to_dict(self):
        entity = super().to_dict()
        entity["type"] = "coin"
        return entity
