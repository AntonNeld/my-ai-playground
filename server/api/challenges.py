from typing import List

from fastapi import APIRouter

from dungeon.challenge_keeper import Challenge


def challenges_routes(state_keeper):

    router = APIRouter()

    @router.get("/challenges", response_model=List[str])
    async def list_challenges():
        return state_keeper.challenge_keeper.list_challenges()

    @router.post("/challenges", response_model=str)
    async def create_challenge(challenge: Challenge):
        return state_keeper.challenge_keeper.add_challenge(challenge)

    @router.get("/challenges/{challenge_id}", response_model=Challenge,
                response_model_exclude_none=True)
    async def get_challenge(challenge_id: str):
        return state_keeper.challenge_keeper.get_challenge(challenge_id)

    @router.put("/challenges/{challenge_id}", response_model=str)
    async def create_challenge_with_id(challenge_id: str,
                                       challenge: Challenge):
        return state_keeper.challenge_keeper.add_challenge(
            challenge,
            challenge_id=challenge_id)

    @router.delete("/challenges/{challenge_id}")
    async def delete_challenge(challenge_id: str):
        return state_keeper.challenge_keeper.remove_challenge_by_id(
            challenge_id)

    @router.get("/challenges/{challenge_id}/variants",
                response_model=List[str])
    async def get_challenge_variants(challenge_id: str):
        challenge = state_keeper.challenge_keeper.get_challenge(challenge_id)
        if challenge.variants is not None:
            return list(challenge.variants.keys())
        return []

    return router
