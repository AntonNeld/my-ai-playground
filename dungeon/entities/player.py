import requests
import json

AI_URL = "http://127.0.0.1:5100/api/nextmove"


class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.looks_like = "player"

    def step(self):
        r = requests.get(AI_URL)
        action = json.loads(r.text)
        if action == "move_up":
            self.y += 1
        elif action == "move_down":
            self.y -= 1
        elif action == "move_left":
            self.x -= 1
        elif action == "move_right":
            self.x += 1
