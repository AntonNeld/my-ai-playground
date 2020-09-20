from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

from api import create_api
from state import StateKeeper
from errors import ResourceNotFoundError


def create_app(challenge_dir=None, static_dir=None):
    app = FastAPI()
    if static_dir:
        app.mount("/static", StaticFiles(directory=static_dir),
                  name="static")

    state_keeper = StateKeeper(challenge_dir)
    app.include_router(create_api(state_keeper), prefix="/api")

    @app.get("/")
    async def redirect_static():
        return RedirectResponse(url="/static/index.html")

    @app.exception_handler(ResourceNotFoundError)
    async def handle_resource_not_found(request: Request,
                                        exc: ResourceNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"message": "Resource not found"}
        )

    return app
