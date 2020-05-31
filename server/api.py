from typing import List

from fastapi import APIRouter, Body
from pydantic import BaseModel

from dungeon import Dungeon
from dungeon.entities.entity_factories import entity_from_json


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
    id: str = None  # Temporary, will remove id from entity later
    score: int = None


def create_api():

    router = APIRouter()
    dungeon = Dungeon()

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
    async def create_room_with_id(room: str,
                                  room_content: List[EntityTemplate]):
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

    @router.post("/rooms/{room}/entities", response_model=str)
    async def post_entity(room: str, entity: Entity):
        entity_obj = entity_from_json(entity.dict(exclude_none=True))
        dungeon.get_room(room).add_entities(entity_obj)
        return entity_obj.id

    @router.get("/rooms/{room}/entities", response_model=List[str])
    async def list_entities(room: str):
        return dungeon.get_room(room).list_entities()

    @router.get("/rooms/{room}/entities/{entity_id}", response_model=Entity)
    async def get_entity(room: str, entity_id: str):
        return dungeon.get_room(room).get_entity(entity_id).to_json()

    @router.put("/rooms/{room}/entities/{entity_id}")
    async def update_entity(room: str, entity_id: str, entity: Entity):
        return dungeon.get_room(room).update_entity(
            entity_id, entity_from_json(entity.dict()))

    @router.put("/rooms/{room}/agents/{agent}/setmove")
    async def set_move(room: str, agent: str, action: str = Body(...)):
        return dungeon.manual_set_move(room, agent, action)

    return router
