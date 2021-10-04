from fastapi import APIRouter, Response

from handsy.api.models.group import Group
from handsy.api.models.user import User

router = APIRouter()


@router.get("/user/{user_id}/group")
async def get_all_user_groups(user_id):
    return [
        Group(
            id="1",
            user_id=user_id,
            name="Clay craft",
            description="All things related to clay"
        ).dict(),
        Group(
            id="2",
            user_id=user_id,
            name="LeatherNerd",
            description="Leather belts, wallets, etc. all made by me!"
        ).dict()
    ]


@router.get("/user/{user_id}/group/{group_id}")
async def get_user_group(user_id, group_id):
    return Group(
        id=group_id,
        user_id=user_id,
        name="Clay craft",
        description="All things related to clay"
    ).dict()


@router.get("/group")
async def get_all():
    return [
        Group(
            id="1",
            user_id="1",
            name="Clay craft",
            description="All things related to clay"
        ).dict(),
        Group(
            id="2",
            user_id="2",
            name="LeatherNerd",
            description="Leather belts, wallets, etc. all made by me!"
        ).dict()
    ]


@router.get("/group/{id}")
async def get(id: str):
    return Group(
        id=id,
        user_id="1",
        name="Clay craft",
        description="All things related to clay"
    ).dict()


@router.post("/group/")
async def create(id: str, group: Group):
    return Response(status_code=201)


@router.put("/group/{id}")
async def update(id: str, group: Group):
    return Response(status_code=200)


@router.delete("/group/{id}")
async def delete(id: str):
    return Response(status_code=204)
