from .entity import Entity


class Wall(Entity):

    def __init__(self, x, y, entity_id=None):
        super().__init__(x, y, "wall", entity_id=entity_id)

    def to_json(self):
        json = super().to_json()
        json["type"] = "block"
        return json
