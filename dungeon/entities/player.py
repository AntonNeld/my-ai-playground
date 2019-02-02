class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.looks_like = "player"

    def step(self):
        self.x += 1
