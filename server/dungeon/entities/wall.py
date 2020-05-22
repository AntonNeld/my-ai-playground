from .entity import Entity


class Wall(Entity):

    def __init__(self, room, x, y):
        super().__init__(room, x, y, "wall")
