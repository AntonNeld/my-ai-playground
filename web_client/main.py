from typing import Optional, List

from aiohttp import ClientSession
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

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
    async with session.post(
            "http://dungeon:5000/api/room",
            json=[item.dict(exclude_none=True) for item in room_content]
    ) as response:
        return await response.json()


@app.post("/api/room/{room}")
async def create_room_with_id(room: str, room_content: List[Entity]):
    async with session.post(
            f"http://dungeon:5000/api/room/{room}",
            json=[item.dict(exclude_none=True) for item in room_content]
    ) as response:
        return await response.json()


@app.delete("/api/room/{room}")
async def delete_room(room: str):
    async with session.delete(
            f"http://dungeon:5000/api/room/{room}") as response:
        return await response.json()


class EntityView(BaseModel):
    x: int
    y: int
    looks_like: str
    id: str


@app.get("/api/room/{room}/view", response_model=List[EntityView])
async def get_view(room: str):
    async with session.get(
            f"http://dungeon:5000/api/room/{room}/view") as response:
        return await response.json()


class Score(BaseModel):
    id: str
    score: int


@app.get("/api/room/{room}/score", response_model=List[Score])
async def get_score(room: str, agent: Optional[str] = None):
    async with session.get(
            f"http://dungeon:5000/api/room/{room}/score",
            params={"agent": agent} if agent is not None else {}
    ) as response:
        return await response.json()


@app.post("/api/room/{room}/step")
async def step_room(room: str):
    async with session.post(
            f"http://dungeon:5000/api/room/{room}/step") as response:
        return await response.json()


@app.get("/api/room/{room}/step", response_model=int)
async def get_steps(room: str):
    async with session.get(
            f"http://dungeon:5000/api/room/{room}/step") as response:
        return await response.json()


@app.put("/api/manual/agent/{agent}/setmove")
async def set_move(agent: str, action: str = Body(...)):
    async with session.put(
            f"http://dungeon:5000/api/manual/agent/{agent}/setmove",
            json=action) as response:
        return await response.json()
