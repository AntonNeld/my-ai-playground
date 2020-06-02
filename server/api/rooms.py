from typing import List

from fastapi import APIRouter

from dungeon.room import room_from_json
from models import Room


def rooms_routes(dungeon):

    router = APIRouter()

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

    return router
