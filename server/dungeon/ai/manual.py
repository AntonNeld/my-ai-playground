
class ManualAI:

    def __init__(self, plan):
        self._plan = plan

    def next_move(self, percept):
        action = self._plan
        self._plan = "none"
        return action if action is not None else "none"

    def set_move(self, action):
        self._plan = action

    def to_dict(self):
        return {"kind": "manual", "plan": self._plan}
