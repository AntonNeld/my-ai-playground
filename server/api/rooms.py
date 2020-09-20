from typing import List

from fastapi import APIRouter, HTTPException

from dungeon.room import Room


def rooms_routes(state_keeper):

    router = APIRouter()

    @router.get("/rooms", response_model=List[str])
    async def list_rooms():
        return state_keeper.dungeon.list_rooms()

    @router.post("/rooms", response_model=str)
    async def create_room(room: Room = None, from_challenge: str = None):
        if from_challenge:
            room_obj = state_keeper.challenge_keeper.get_challenge(
                from_challenge).create_room()
        elif room:
            room_obj = room
        else:
            raise HTTPException(status_code=422, detail="Unprocessable entity")
        return state_keeper.dungeon.add_room(room_obj)

    @router.get("/rooms/{room_id}", response_model=Room,
                response_model_exclude_none=True)
    async def get_room(room_id: str):
        return state_keeper.dungeon.get_room(room_id)

    @router.put("/rooms/{room_id}", response_model=str)
    async def create_room_with_id(room_id: str,
                                  room: Room = None,
                                  from_challenge: str = None):
        if from_challenge:
            room_obj = state_keeper.challenge_keeper.get_challenge(
                from_challenge).create_room()
        elif room:
            room_obj = room
        else:
            raise HTTPException(status_code=422, detail="Unprocessable entity")
        return state_keeper.dungeon.add_room(room_obj, room_id=room_id)

    @router.delete("/rooms/{room_id}")
    async def delete_room(room_id: str):
        return state_keeper.dungeon.remove_room_by_id(room_id)

    @router.post("/rooms/{room_id}/step")
    async def step_room(room_id: str, steps: int = 1):
        return state_keeper.dungeon.get_room(room_id).step(steps)

    return router
