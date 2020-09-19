from fastapi import APIRouter

from api.templates import templates_routes
from api.rooms import rooms_routes
from api.entities import entities_routes
from api.evaluate import evaluate_routes
from api.state import state_routes


def create_api(state_keeper):

    router = APIRouter()
    router.include_router(templates_routes(state_keeper))
    router.include_router(rooms_routes(state_keeper))
    router.include_router(entities_routes(state_keeper))
    router.include_router(evaluate_routes(state_keeper))
    router.include_router(state_routes(state_keeper))
    return router
