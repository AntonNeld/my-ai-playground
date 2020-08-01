from pydantic import BaseModel

from typing_extensions import Literal


class HeldItemsScoring(BaseModel):
    kind: Literal["heldItems"]

    def get_score(self, entity, room):
        if entity.can_pickup is None:
            return 0
        return len(entity.can_pickup.inventory)
