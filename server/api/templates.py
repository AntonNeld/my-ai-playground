from typing import List

from fastapi import APIRouter

from dungeon.templating import Template


def templates_routes(state_keeper):

    router = APIRouter()

    @router.get("/templates", response_model=List[str])
    async def list_templates():
        return state_keeper.template_keeper.list_templates()

    @router.post("/templates", response_model=str)
    async def create_template(template: Template):
        return state_keeper.template_keeper.add_template(template)

    @router.get("/templates/{template_id}", response_model=Template,
                response_model_exclude_none=True)
    async def get_template(template_id: str):
        return state_keeper.template_keeper.get_template(template_id)

    @router.put("/templates/{template_id}", response_model=str)
    async def create_template_with_id(template_id: str,
                                      template: Template):
        return state_keeper.template_keeper.add_template(
            template,
            template_id=template_id)

    @router.delete("/templates/{template_id}")
    async def delete_template(template_id: str):
        return state_keeper.template_keeper.remove_template_by_id(template_id)

    return router
