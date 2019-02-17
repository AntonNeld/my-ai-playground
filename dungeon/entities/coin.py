from .entity import Entity


class Coin(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, "coin")
        self.solid = False
