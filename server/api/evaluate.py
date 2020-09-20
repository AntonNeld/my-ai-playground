from typing import Dict, Optional

from pydantic import BaseModel, Field
from fastapi import APIRouter

from profiling import time_profiling, memory_profiling


class EvaluateBody(BaseModel):
    challenge: str
    duration: int
    profile_time: bool = Field(False, alias="profileTime")
    profile_memory: bool = Field(False, alias="profileMemory")


class EvaluateResponse(BaseModel):
    scores: Dict[str, int]
    process_time: Optional[float] = Field(None, alias="processTime")
    ai_times: Optional[Dict[str, float]] = Field(None, alias="aiTimes")
    ai_memory: Optional[Dict[str, float]] = Field(None, alias="aiMemory")


def evaluate_routes(state_keeper):

    router = APIRouter()

    @router.post("/evaluate", response_model=EvaluateResponse,
                 response_model_exclude_none=True)
    async def evaluate(body: EvaluateBody):
        room = state_keeper.challenge_keeper.get_challenge(
            body.challenge).create_room()
        if body.profile_time:
            time_profiling.start()
        if body.profile_memory:
            memory_profiling.start()
        room.step(steps=body.duration)
        if body.profile_time:
            time_profiling.stop()
        if body.profile_memory:
            memory_profiling.stop()
        scores = {}
        for entity in room.get_entities():
            if entity.label is not None:
                scores[entity.label] = room.get_entity_score(entity)
        result = {"scores": scores}
        if body.profile_time:
            profile_result = time_profiling.get_result()
            result["processTime"] = profile_result["process_time"]
            result["aiTimes"] = profile_result["contexts"]
        if body.profile_memory:
            profile_result = memory_profiling.get_result()
            result["aiMemory"] = profile_result
        return result

    return router
