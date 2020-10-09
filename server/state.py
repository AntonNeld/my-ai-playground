import json
import yaml
from pathlib import Path

from dungeon.dungeon import Dungeon
from dungeon.challenge_keeper import ChallengeKeeper, Challenge


class StateKeeper:

    def __init__(self, challenge_dir):
        self._challenge_dir = challenge_dir
        self.clear_state()

    def clear_state(self):
        self.dungeon = Dungeon()
        self.challenge_keeper = ChallengeKeeper()
        if self._challenge_dir:
            self.load_challenge_directory()

    def load_challenge_directory(self):
        parent_dir = Path(self._challenge_dir)
        for p in parent_dir.glob("./*.json"):
            with p.open() as f:
                challenge = Challenge(**json.load(f))
                self.challenge_keeper.add_challenge(
                    challenge, challenge_id=p.stem)
        for p in parent_dir.glob("./*.yaml"):
            with p.open() as f:
                challenge = Challenge(**yaml.safe_load(f))
                self.challenge_keeper.add_challenge(
                    challenge, challenge_id=p.stem)
