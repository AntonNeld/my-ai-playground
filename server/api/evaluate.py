from typing import Dict, Optional

from pydantic import BaseModel, Field
from fastapi import APIRouter

from profiling import time_profiling


class EvaluateBody(BaseModel):
    template: str
    duration: int
    profile_time: bool = Field(False, alias="profileTime")


class EvaluateResponse(BaseModel):
    scores: Dict[str, int]
    process_time: Optional[float] = Field(None, alias="processTime")


def evaluate_routes(dungeon, template_keeper):

    router = APIRouter()

    @router.post("/evaluate", response_model=EvaluateResponse,
                 response_model_exclude_none=True)
    async def evaluate(body: EvaluateBody):
        room = template_keeper.get_template(
            body.template).create_room()
        if body.profile_time:
            time_profiling.start()
        room.step(steps=body.duration)
        if body.profile_time:
            time_profiling.stop()
        scores = {}
        for entity in room.get_entities():
            if entity.label is not None:
                scores[entity.label] = room.get_entity_score(entity)
        result = {"scores": scores}
        if body.profile_time:
            profile_result = time_profiling.get_result()
            result["processTime"] = profile_result["process_time"]
        return result

    return router
