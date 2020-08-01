from pydantic import BaseModel

from typing_extensions import Literal


class HeldItemsScoring(BaseModel):
    kind: Literal["heldItems"]

    def get_score(self, entity, room):
        if entity.pickupper is None:
            return 0
        return len(entity.pickupper.inventory)
