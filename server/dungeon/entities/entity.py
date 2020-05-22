import uuid


class Entity:

    def __init__(self, room, x, y, looks_like):
        self.room = room
        self.x = x
        self.y = y
        self.looks_like = looks_like
        self.id = uuid.uuid4().hex
        self.solid = True

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "id": self.id
        }
