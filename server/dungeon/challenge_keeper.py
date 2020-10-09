from typing import Dict, Any, Optional
import uuid

from pydantic import BaseModel
import jsonpath_ng

from errors import ResourceNotFoundError
from dungeon.template import Template


class Challenge(BaseModel):
    variants: Optional[Dict[str, Dict[str, Any]]]
    template: Template

    def create_room(self, variant=None):
        if variant is None:
            return self.template.create_room()
        template_dict = self.template.dict(by_alias=True)
        for path, value in self.variants[variant].items():
            path_expression = jsonpath_ng.parse(path)
            template_dict = path_expression.update(template_dict, value)
        TemplateClass = self.template.__class__
        template = TemplateClass(**template_dict)
        return template.create_room()


class ChallengeKeeper:

    def __init__(self):
        self._challenges = {}

    def add_challenge(self, challenge, challenge_id=None):
        if challenge_id is None:
            challenge_id = uuid.uuid4().hex
        self._challenges[challenge_id] = challenge
        return challenge_id

    def get_challenge(self, challenge_id):
        try:
            return self._challenges[challenge_id]
        except KeyError:
            raise ResourceNotFoundError

    def remove_challenge_by_id(self, challenge_id):
        if challenge_id in self._challenges:
            del self._challenges[challenge_id]

    def list_challenges(self):
        return list(self._challenges.keys())
