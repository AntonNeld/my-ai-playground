from .entity import Entity


class Coin(Entity):

    def __init__(self, room, x, y):
        super().__init__(room, x, y, "coin")
        self.solid = False

    def to_json(self):
        json = super().to_json()
        json["type"] = "coin"
        return json
