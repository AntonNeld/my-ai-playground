from .entity import Entity


class Wall(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, "wall")

    def to_json(self):
        json = super().to_json()
        json["type"] = "block"
        return json
