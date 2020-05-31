import os.path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from api import create_api


def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory=os.path.join(
        os.path.dirname(__file__), "static")), name="static")
    app.include_router(create_api(), prefix="/api")
    return app

    @app.get("/")
    async def redirect_static():
        return RedirectResponse(url="/static/index.html")


app = create_app()
