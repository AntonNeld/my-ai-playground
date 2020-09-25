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
        challenge = state_keeper.challenge_keeper.get_challenge(
            body.challenge)
        response = {"entities": {}}
        for variant in challenge.variants or [None]:
            room = state_keeper.challenge_keeper.get_challenge(
                body.challenge).create_room(variant=variant)

            if body.profile_time:
                time_profiling.start()
            if body.profile_memory:
                memory_profiling.start()
            room.step(steps=body.duration)
            if body.profile_time:
                time_profiling.stop()
                time_result = time_profiling.get_result()
                if "processTime" not in response:
                    response["processTime"] = 0
                response["processTime"] += time_result["process_time"]
            if body.profile_memory:
                memory_profiling.stop()
                memory_result = memory_profiling.get_result()

            for entity in [e for e in room.get_entities()
                           if e.label is not None]:
                label = (entity.label if variant is None
                         else f"{variant}:{entity.label}")
                response["entities"][label] = {
                    "score": room.get_entity_score(entity)
                }
                if body.profile_time:
                    if entity.label in time_result["contexts"]:
                        ai_time = time_result["contexts"][entity.label]
                    else:
                        ai_time = 0
                    response["entities"][label]["time"] = ai_time
                if body.profile_memory:
                    if entity.label in memory_result:
                        ai_memory = memory_result[entity.label]
                    else:
                        ai_memory = 0
                    response["entities"][label]["memory"] = ai_memory
        return response

    return router
