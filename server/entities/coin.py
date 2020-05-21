from .entity import Entity


class Coin(Entity):

    def __init__(self, room, x, y):
        super().__init__(room, x, y, "coin")
        self.solid = False
