import uuid


class Entity:

    def __init__(self, room, x, y, looks_like):
        self.room = room
        self.x = x
        self.y = y
        self.looks_like = looks_like
        self.id = uuid.uuid4().hex
        self.solid = True
