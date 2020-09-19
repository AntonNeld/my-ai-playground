from fastapi import APIRouter


def state_routes(state_keeper):

    router = APIRouter()

    @router.post("/state/clear")
    async def clear():
        return state_keeper.clear_state()

    return router
