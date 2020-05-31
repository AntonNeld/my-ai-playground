from typing import List, Dict

from fastapi import APIRouter, Body
from pydantic import BaseModel

from dungeon import Dungeon
from dungeon.entities.entity_factories import entity_from_json


class Entity(BaseModel):
    x: int
    y: int
    type: str
    ai: str = None
    score: int = None


class Room(BaseModel):
    entities: Dict[str, Entity]


def create_api():

    router = APIRouter()
    dungeon = Dungeon()

    @router.get("/rooms", response_model=List[str])
    async def get_rooms():
        return dungeon.list_rooms()

    @router.post("/rooms", response_model=str)
    async def create_room(room: Room):
        return dungeon.create_room(room.dict(exclude_none=True))

    @router.get("/rooms/{room_id}", response_model=Room,
                response_model_exclude_none=True)
    async def get_room(room_id: str):
        return dungeon.get_room(room_id).to_json()

    @router.put("/rooms/{room_id}", response_model=str)
    async def create_room_with_id(room_id: str,
                                  room: Room):
        return dungeon.create_room(room.dict(exclude_none=True),
                                   room_id=room_id)

    @router.delete("/rooms/{room_id}")
    async def delete_room(room_id: str):
        return dungeon.delete_room(room_id)

    @router.post("/rooms/{room_id}/step")
    async def step_room(room_id: str):
        return dungeon.step(room_id)

    @router.get("/rooms/{room_id}/step", response_model=int)
    async def get_steps(room_id: str):
        return dungeon.get_steps(room_id)

    @router.post("/rooms/{room_id}/entities", response_model=str)
    async def post_entity(room_id: str, entity: Entity):
        entity_obj = entity_from_json(entity.dict(exclude_none=True))
        entity_id = dungeon.get_room(room_id).add_entity(entity_obj)
        return entity_id

    @router.get("/rooms/{room_id}/entities", response_model=List[str])
    async def list_entities(room_id: str):
        return dungeon.get_room(room_id).list_entities()

    @router.get("/rooms/{room_id}/entities/{entity_id}", response_model=Entity)
    async def get_entity(room_id: str, entity_id: str):
        return dungeon.get_room(room_id).get_entity(entity_id).to_json()

    @router.put("/rooms/{room_id}/entities/{entity_id}")
    async def update_entity(room_id: str, entity_id: str, entity: Entity):
        return dungeon.get_room(room_id).add_entity(
            entity_from_json(entity.dict(exclude_none=True)),
            entity_id=entity_id)

    @router.put("/rooms/{room_id}/agents/{agent_id}/setmove")
    async def set_move(room_id: str, agent_id: str, action: str = Body(...)):
        return dungeon.manual_set_move(room_id, agent_id, action)

    return router
