from typing import Dict

from pydantic import BaseModel
from fastapi import APIRouter


class EvaluateBody(BaseModel):
    template: str
    duration: int


def evaluate_routes(dungeon, template_keeper):

    router = APIRouter()

    @router.post("/evaluate", response_model=Dict[str, int])
    async def evaluate(body: EvaluateBody):
        room = template_keeper.get_template(
            body.template).create_room()
        room.step(steps=body.duration)
        result = {}
        for entity in room.get_entities():
            if entity.label is not None:
                result[entity.label] = room.get_entity_score(entity)
        return result

    return router
