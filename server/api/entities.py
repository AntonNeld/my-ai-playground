from typing import List, Union

from fastapi import APIRouter


from dungeon.entity import Entity


def entities_routes(dungeon):

    router = APIRouter()

    @router.post("/rooms/{room_id}/entities", response_model=str)
    async def post_entity(room_id: str, entity: Entity):
        return dungeon.get_room(room_id).add_entity(entity)

    @router.get("/rooms/{room_id}/entities", response_model=List[str])
    async def list_entities(room_id: str):
        return dungeon.get_room(room_id).list_entities()

    @router.get("/rooms/{room_id}/entities/{entity_id}", response_model=Entity,
                response_model_exclude_none=True)
    async def get_entity(room_id: str, entity_id: str):
        return dungeon.get_room(room_id).get_entity(entity_id)

    @router.put("/rooms/{room_id}/entities/{entity_id}")
    async def put_entity(room_id: str, entity_id: str, entity: Entity):
        return dungeon.get_room(room_id).add_entity(
            entity, entity_id=entity_id)

    @router.delete("/rooms/{room_id}/entities/{entity_id}")
    async def delete_entity(room_id: str, entity_id: str):
        return dungeon.get_room(room_id).remove_entity_by_id(entity_id)

    @router.get("/rooms/{room_id}/entities/{entity_id}/score",
                response_model=int)
    async def get_entity_score(room_id: str, entity_id: Union[str, None]):
        room = dungeon.get_room(room_id)
        entity = room.get_entity(entity_id)
        return (None if entity.scoring is None
                else entity.scoring.get_score(entity, room))

    return router
