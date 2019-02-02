import requests
import json
import room

AI_URL = "http://127.0.0.1:5100/api/nextmove"


class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.looks_like = "player"
        self.solid = False
        self.score = 0

    def step(self):
        r = requests.get(AI_URL)
        action = json.loads(r.text)
        dx = dy = 0

        if action == "move_up":
            dy = 1
        elif action == "move_down":
            dy = -1
        elif action == "move_left":
            dx = -1
        elif action == "move_right":
            dx = 1

        if not room.default_room.is_wall(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

        for thing in room.default_room.get_things():
            if thing.looks_like == "coin" and thing.x == self.x and thing.y == self.y:
                room.default_room.remove_things(thing)
                score += 1
