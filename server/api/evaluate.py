from typing import Dict, Optional

from pydantic import BaseModel, Field
from fastapi import APIRouter

from profiling import time_profiling, memory_profiling


class EvaluateBody(BaseModel):
    challenge: str
    duration: int
    profile_time: bool = Field(False, alias="profileTime")
    profile_memory: bool = Field(False, alias="profileMemory")


class EvaluateEntityInfo(BaseModel):
    score: int
    time: Optional[float]
    memory: Optional[float]


class EvaluateResponse(BaseModel):
    process_time: Optional[float] = Field(None, alias="processTime")
    entities: Dict[str, EvaluateEntityInfo]


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
        result = {
            "entities": {
                e.label: {
                    "score": room.get_entity_score(e),
                    # Initialize time and memory to 0, in case there is no AI
                    # to measure
                    "time": 0 if body.profile_time else None,
                    "memory": 0 if body.profile_memory else None
                }
                for e in room.get_entities()
                if e.label is not None
            }
        }
        if body.profile_time:
            profile_result = time_profiling.get_result()
            result["processTime"] = profile_result["process_time"]
            for entity, entity_time in profile_result["contexts"].items():
                if entity in result["entities"]:
                    result["entities"][entity]["time"] = entity_time
        if body.profile_memory:
            profile_result = memory_profiling.get_result()
            for entity, entity_memory in profile_result.items():
                if entity in result["entities"]:
                    result["entities"][entity]["memory"] = entity_memory
        return result

    return router
