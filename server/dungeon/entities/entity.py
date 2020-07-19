
class Entity:

    def __init__(self, x, y, looks_like, collision_behavior=None):
        self.x = x
        self.y = y
        self.looks_like = looks_like
        self.collision_behavior = collision_behavior

    def set_room(self, room):
        self.room = room

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "looksLike": self.looks_like,
            "collisionBehavior": self.collision_behavior
        }
