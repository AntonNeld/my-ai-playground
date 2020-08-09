from typing import Tuple, Dict

from pydantic import BaseModel, Field
from typing_extensions import Literal

from dungeon.consts import Move
from dungeon.ai.lib.pathfinding import shortest_breadth_first


class ExploringVacuumAI(BaseModel):
    # Exploring vacuum cleaner agent for exercise 2.11d.
    kind: Literal["exploringVacuum"]
    passable: Dict[str, bool] = {}
    position: Tuple[int, int] = (0, 0)
    last_move: Move = Field("none", alias="lastMove")

    def update_state_percept(self, percept):
        x = percept["position"]["x"]
        y = percept["position"]["y"]
        if self.position != (x, y):
            self.position = (x, y)
            self.passable[str((x, y))] = True
        elif self.last_move == "move_up":
            self.passable[str((x, y+1))] = False
        elif self.last_move == "move_down":
            self.passable[str((x, y-1))] = False
        elif self.last_move == "move_left":
            self.passable[str((x-1, y))] = False
        elif self.last_move == "move_right":
            self.passable[str((x+1, y))] = False

    def next_move(self, percept):
        if {"x": 0, "y": 0, "looks_like": "dirt"} in percept["entities"]:
            return "pick_up"

        targets = set()
        obstructions = set()

        for key in self.passable:
            coords = key[1:-1].split(",")
            x = int(coords[0])
            y = int(coords[1])
            if self.passable[key]:
                for pos in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                    if str(pos) not in self.passable:
                        targets.add(pos)
            else:
                obstructions.add((x, y))

        my_x = percept["position"]["x"]
        my_y = percept["position"]["y"]
        return shortest_breadth_first((my_x, my_y), targets, obstructions)[0]

    def update_state_action(self, action):
        self.last_move = action
