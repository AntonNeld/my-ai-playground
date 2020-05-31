import os.path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

from api import create_api
from errors import ResourceNotFoundError


def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory=os.path.join(
        os.path.dirname(__file__), "static")), name="static")
    app.include_router(create_api(), prefix="/api")

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


app = create_app()
