from fastapi import APIRouter

from api.templates import templates_routes
from api.rooms import rooms_routes
from api.entities import entities_routes


def create_api(dungeon, template_keeper):

    router = APIRouter()
    router.include_router(templates_routes(template_keeper))
    router.include_router(rooms_routes(dungeon, template_keeper))
    router.include_router(entities_routes(dungeon))

    return router
