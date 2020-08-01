from typing import List

from pydantic import BaseModel, Field
from typing_extensions import Literal


class TileTagsScoring(BaseModel):
    kind: Literal["tileTags"]
    should_have_tags: List[str] = Field([], alias="shouldHaveTags")
    should_not_have_tags: List[str] = Field([], alias="shouldNotHaveTags")

    def get_score(self, entity, room):
        positions = map(lambda e: e.position,
                        room.get_entities())
        score = 0
        for position in positions:
            entities = room.get_entities(position=position)
            if (all(map(lambda t: tag_in_entities(t, entities),
                        self.should_have_tags))
                    and not any(map(lambda t: tag_in_entities(t, entities),
                                    self.should_not_have_tags))):
                score += 1
        return score


def tag_in_entities(tag, entities):
    for entity in entities:
        if entity.tags is not None and tag in entity.tags:
            return True
    return False