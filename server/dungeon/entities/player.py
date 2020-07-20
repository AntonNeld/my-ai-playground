from .entity import Entity


class Player(Entity):

    def __init__(self, x, y, ai, score):
        super().__init__(x, y, "player")
        self.ai = ai
        self.score = score

    def to_dict(self):
        entity = super().to_dict()
        entity["ai"] = self.ai.to_dict()
        entity["score"] = self.score
        return entity
