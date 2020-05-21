from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from api import router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix="/api")


@app.get("/")
async def redirect_static():
    return RedirectResponse(url="/static/index.html")
