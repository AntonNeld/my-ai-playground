from .entity import Entity


class Player(Entity):

    def __init__(self, x, y, ai, score):
        super().__init__(x, y, "player")
        self.ai = ai
        self.score = score

    def step(self, action="none"):
        dx = dy = 0

        if action == "move_up":
            dy = 1
        elif action == "move_down":
            dy = -1
        elif action == "move_left":
            dx = -1
        elif action == "move_right":
            dx = 1

        if self.room.passable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

        for entity in self.room.get_entities():
            if entity.x == self.x and entity.y == self.y:
                if entity.collision_behavior == "vanish":
                    self.room.remove_entity(entity)
                    if entity.score_on_destroy is not None:
                        if self.score is None:
                            self.score = 0
                        self.score += entity.score_on_destroy

    def to_dict(self):
        entity = super().to_dict()
        entity["ai"] = self.ai.to_dict()
        entity["score"] = self.score
        return entity
