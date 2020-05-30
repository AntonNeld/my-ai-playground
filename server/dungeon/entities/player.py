from .coin import Coin
from .entity import Entity


class Player(Entity):

    def __init__(self, x, y, ai):
        super().__init__(x, y, "player")
        self.ai = ai
        self.score = 0

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
            if (isinstance(entity, Coin) and entity.x == self.x
                    and entity.y == self.y):
                self.room.remove_entities(entity)
                self.score += 1

    def to_json(self):
        json = super().to_json()
        json["type"] = "player"
        json["ai"] = self.ai.to_json()
        json["score"] = self.score
        return json
