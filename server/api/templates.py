from typing import List

from fastapi import APIRouter

from models import Template


def templates_routes(dungeon):

    router = APIRouter()

    @router.get("/templates", response_model=List[str])
    async def list_templates():
        return dungeon.list_templates()

    @router.post("/templates", response_model=str)
    async def create_template(template: Template):
        return dungeon.add_template(template.dict())

    @router.get("/templates/{template_id}", response_model=Template)
    async def get_template(template_id: str):
        return dungeon.get_template(template_id)

    @router.put("/templates/{template_id}", response_model=str)
    async def create_template_with_id(template_id: str,
                                      template: Template):
        return dungeon.add_template(template.dict(), template_id=template_id)

    @router.delete("/templates/{template_id}")
    async def delete_template(template_id: str):
        return dungeon.remove_template_by_id(template_id)

    return router
