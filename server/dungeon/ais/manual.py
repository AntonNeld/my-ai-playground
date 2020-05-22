
class ManualAI:

    def __init__(self):
        self._plan = "none"

    def next_move(self, percept):
        return self._plan

    def set_move(self, action):
        self._plan = action
