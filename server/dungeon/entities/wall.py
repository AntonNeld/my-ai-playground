from .entity import Entity


class Wall(Entity):

    def __init__(self, room, x, y):
        super().__init__(room, x, y, "wall")

    def to_json(self):
        json = super().to_json()
        json["type"] = "block"
        return json
