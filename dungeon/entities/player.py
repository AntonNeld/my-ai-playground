import requests
import json
import os
import room

if "DUNGEON_PLAYER_AI" in os.environ:
    ai_host = os.environ["DUNGEON_PLAYER_AI"]
else:
    ai_host = "127.0.0.1"
AI_URL = "http://" + ai_host + ":5100/api/nextmove"


class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.looks_like = "player"
        self.solid = False

    def step(self):
        r = requests.post(AI_URL, json=room.get_current_room().get_view(self))
        action = json.loads(r.text)

        room.get_current_room().steps += 1
        dx = dy = 0

        if action == "move_up":
            dy = 1
        elif action == "move_down":
            dy = -1
        elif action == "move_left":
            dx = -1
        elif action == "move_right":
            dx = 1

        if not room.get_current_room().is_wall(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

        for thing in room.get_current_room().get_things():
            if (thing.looks_like == "coin" and thing.x == self.x
                    and thing.y == self.y):
                room.get_current_room().remove_things(thing)
                room.get_current_room().score += 1
