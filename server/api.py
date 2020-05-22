from typing import Optional, List

from fastapi import APIRouter, Body
from pydantic import BaseModel

import endpoint

router = APIRouter()


# Legacy API used by pyglet client

class Entity(BaseModel):
    x: int
    y: int
    type: str
    ai: str = None


@router.post("/room", response_model=str)
async def create_room(room_content: List[Entity]):
    return endpoint.create_room([item.dict(exclude_none=True)
                                 for item in room_content])


@router.post("/room/{room}")
async def create_room_with_id(room: str, room_content: List[Entity]):
    return endpoint.create_room_with_id(room, [item.dict(exclude_none=True)
                                               for item in room_content])


@router.delete("/room/{room}")
async def delete_room(room: str):
    return endpoint.delete_room(room)


class EntityView(BaseModel):
    x: int
    y: int
    looks_like: str
    id: str


@router.get("/room/{room}/view", response_model=List[EntityView])
async def get_view(room: str):
    return endpoint.get_view(room)


class Score(BaseModel):
    id: str
    score: int


@router.get("/room/{room}/score", response_model=List[Score])
async def get_score(room: str, agent: Optional[str] = None):
    return endpoint.get_score(room, agent)


@router.post("/room/{room}/step")
async def step_room(room: str):
    return endpoint.step(room)


@router.get("/room/{room}/step", response_model=int)
async def get_steps(room: str):
    return endpoint.get_steps(room)


@router.put("/manual/agent/{agent}/setmove")
async def set_move(agent: str, action: str = Body(...)):
    return endpoint.manual_set_move(agent, action)