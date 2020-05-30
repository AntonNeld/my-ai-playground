import uuid


class Entity:

    def __init__(self, x, y, looks_like, entity_id=None):
        self.x = x
        self.y = y
        self.looks_like = looks_like
        self.id = uuid.uuid4().hex if entity_id is None else entity_id
        self.solid = True

    def set_room(self, room):
        self.room = room

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "id": self.id
        }
