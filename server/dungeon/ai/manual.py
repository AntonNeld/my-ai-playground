
class ManualAI:

    def __init__(self):
        self._plan = "none"

    def next_move(self, percept):
        action = self._plan
        self._plan = "none"
        return action

    def set_move(self, action):
        self._plan = action

    def to_dict(self):
        return "manual"
