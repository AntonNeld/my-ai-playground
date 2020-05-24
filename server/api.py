from typing import List

from fastapi import APIRouter, Body
from pydantic import BaseModel

from dungeon import Dungeon

router = APIRouter()

dungeon = Dungeon()

# Legacy API used by pyglet client


class EntityTemplate(BaseModel):
    x: int
    y: int
    type: str
    ai: str = None


class Entity(BaseModel):
    x: int
    y: int
    type: str
    ai: str = None
    id: str
    score: int = None


@router.get("/rooms", response_model=List[str])
async def get_rooms():
    print(dungeon.list_rooms())
    return dungeon.list_rooms()


@router.post("/rooms", response_model=str)
async def create_room(room_content: List[EntityTemplate]):
    return dungeon.create_room([item.dict(exclude_none=True)
                                for item in room_content])


@router.get("/rooms/{room}", response_model=List[Entity],
            response_model_exclude_none=True)
async def get_room(room: str):
    return dungeon.get_room(room).to_json()


@router.put("/rooms/{room}", response_model=str)
async def create_room_with_id(room: str, room_content: List[EntityTemplate]):
    return dungeon.create_room([item.dict(exclude_none=True)
                                for item in room_content], room_id=room)


@router.delete("/rooms/{room}")
async def delete_room(room: str):
    return dungeon.delete_room(room)


@router.post("/rooms/{room}/step")
async def step_room(room: str):
    return dungeon.step(room)


@router.get("/rooms/{room}/step", response_model=int)
async def get_steps(room: str):
    return dungeon.get_steps(room)


@router.put("/rooms/{room}/agents/{agent}/setmove")
async def set_move(room: str, agent: str, action: str = Body(...)):
    return dungeon.manual_set_move(room, agent, action)
