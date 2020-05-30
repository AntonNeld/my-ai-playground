from .entity import Entity


class Coin(Entity):

    def __init__(self, x, y, entity_id=None):
        super().__init__(x, y, "coin", entity_id=entity_id)
        self.solid = False

    def to_json(self):
        json = super().to_json()
        json["type"] = "coin"
        return json
