from dungeon.dungeon import Dungeon
from dungeon.challenge_keeper import ChallengeKeeper


class StateKeeper:

    def __init__(self, challenge_dir):
        self._challenge_dir = challenge_dir
        self.clear_state()

    def clear_state(self):
        self.dungeon = Dungeon()
        self.challenge_keeper = ChallengeKeeper()
        if self._challenge_dir:
            self.challenge_keeper.load_directory(self._challenge_dir)
