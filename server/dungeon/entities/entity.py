
class Entity:

    def __init__(self, x, y, looks_like):
        self.x = x
        self.y = y
        self.looks_like = looks_like
        self.solid = True

    def set_room(self, room):
        self.room = room

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y
        }
