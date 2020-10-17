from typing import List

from pydantic import BaseModel, Field
from typing_extensions import Literal


class TileTagsScoring(BaseModel):
    kind: Literal["tileTags"]
    score: int = 1
    should_have_tags: List[str] = Field([], alias="shouldHaveTags")
    should_not_have_tags: List[str] = Field([], alias="shouldNotHaveTags")

    def get_score(self, entity, room):
        positions = [e.position for e in room.get_entities()
                     if e.position is not None]
        score = 0
        done_positions = set()
        for position in positions:
            if (position.x, position.y) in done_positions:
                continue
            entities = room.get_entities(position=position)
            if (all(map(lambda t: tag_in_entities(t, entities),
                        self.should_have_tags))
                    and not any(map(lambda t: tag_in_entities(t, entities),
                                    self.should_not_have_tags))):
                score += self.score
            done_positions.add((position.x, position.y))
        return score


def tag_in_entities(tag, entities):
    for entity in entities:
        if tag in entity.get_tags():
            return True
    return False
