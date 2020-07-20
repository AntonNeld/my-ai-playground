
class Entity:

    def __init__(self, x, y, looksLike, collisionBehavior=None,
                 scoreOnDestroy=None):
        self.x = x
        self.y = y
        self.looks_like = looksLike
        self.collision_behavior = collisionBehavior
        self.score_on_destroy = scoreOnDestroy

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "looksLike": self.looks_like,
            "collisionBehavior": self.collision_behavior,
            "scoreOnDestroy": self.score_on_destroy
        }
