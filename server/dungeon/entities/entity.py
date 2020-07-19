
class Entity:

    def __init__(self, x, y, looks_like, solid):
        self.x = x
        self.y = y
        self.looks_like = looks_like
        self.solid = solid

    def set_room(self, room):
        self.room = room

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "looksLike": self.looks_like,
            "solid": self.solid
        }
