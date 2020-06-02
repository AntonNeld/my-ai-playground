from typing import List

from fastapi import APIRouter, Body


from dungeon import Dungeon
from dungeon.entities.entity_factories import entity_from_json
from dungeon.room import room_from_json
from models import Room, Entity


def create_api():

    router = APIRouter()
    dungeon = Dungeon()

    @router.get("/rooms", response_model=List[str])
    async def list_rooms():
        return dungeon.list_rooms()

    @router.post("/rooms", response_model=str)
    async def create_room(room: Room):
        room_obj = room_from_json(room.dict())
        return dungeon.add_room(room_obj)

    @router.get("/rooms/{room_id}", response_model=Room)
    async def get_room(room_id: str):
        return dungeon.get_room(room_id).to_json()

    @router.put("/rooms/{room_id}", response_model=str)
    async def create_room_with_id(room_id: str,
                                  room: Room):
        room_obj = room_from_json(room.dict())
        return dungeon.add_room(room_obj, room_id=room_id)

    @router.delete("/rooms/{room_id}")
    async def delete_room(room_id: str):
        return dungeon.remove_room_by_id(room_id)

    @router.post("/rooms/{room_id}/step")
    async def step_room(room_id: str):
        return dungeon.get_room(room_id).step()

    @router.post("/rooms/{room_id}/entities", response_model=str)
    async def post_entity(room_id: str, entity: Entity):
        entity_obj = entity_from_json(entity.dict())
        return dungeon.get_room(room_id).add_entity(entity_obj)

    @router.get("/rooms/{room_id}/entities", response_model=List[str])
    async def list_entities(room_id: str):
        return dungeon.get_room(room_id).list_entities()

    @router.get("/rooms/{room_id}/entities/{entity_id}", response_model=Entity)
    async def get_entity(room_id: str, entity_id: str):
        return dungeon.get_room(room_id).get_entity(entity_id).to_json()

    @router.put("/rooms/{room_id}/entities/{entity_id}")
    async def put_entity(room_id: str, entity_id: str, entity: Entity):
        entity_obj = entity_from_json(entity.dict())
        return dungeon.get_room(room_id).add_entity(
            entity_obj, entity_id=entity_id)

    @router.delete("/rooms/{room_id}/entities/{entity_id}")
    async def delete_entity(room_id: str, entity_id: str):
        return dungeon.get_room(room_id).remove_entity_by_id(entity_id)

    @router.put("/rooms/{room_id}/entities/{agent_id}/setmove")
    async def set_move(room_id: str, agent_id: str, action: str = Body(...)):
        return dungeon.manual_set_move(room_id, agent_id, action)

    return router
