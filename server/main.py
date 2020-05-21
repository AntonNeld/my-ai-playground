from typing import Optional, List

from aiohttp import ClientSession
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

import endpoint

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

session = ClientSession()


@app.get("/")
async def redirect_static():
    return RedirectResponse(url="/static/index.html")


# Legacy API used by pyglet client

class Entity(BaseModel):
    x: int
    y: int
    type: str
    ai: str = None


@app.post("/api/room", response_model=str)
async def create_room(room_content: List[Entity]):
    return endpoint.create_room([item.dict(exclude_none=True)
                                 for item in room_content])


@app.post("/api/room/{room}")
async def create_room_with_id(room: str, room_content: List[Entity]):
    return endpoint.create_room_with_id(room, [item.dict(exclude_none=True)
                                               for item in room_content])


@app.delete("/api/room/{room}")
async def delete_room(room: str):
    return endpoint.delete_room(room)


class EntityView(BaseModel):
    x: int
    y: int
    looks_like: str
    id: str


@app.get("/api/room/{room}/view", response_model=List[EntityView])
async def get_view(room: str):
    return endpoint.get_view(room)


class Score(BaseModel):
    id: str
    score: int


@app.get("/api/room/{room}/score", response_model=List[Score])
async def get_score(room: str, agent: Optional[str] = None):
    return endpoint.get_score(room, agent)


@app.post("/api/room/{room}/step")
async def step_room(room: str):
    return endpoint.step(room)


@app.get("/api/room/{room}/step", response_model=int)
async def get_steps(room: str):
    return endpoint.get_steps(room)


@app.put("/api/manual/agent/{agent}/setmove")
async def set_move(agent: str, action: str = Body(...)):
    return endpoint.manual_set_move(agent, action)
