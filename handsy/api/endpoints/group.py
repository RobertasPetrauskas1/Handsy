from fastapi import APIRouter, Response

from handsy.api.models.group import Group
from handsy.api.models.user import User

router = APIRouter(prefix="/group")


@router.get("/")
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


@router.get("/{id}")
async def get(id: str):
    return Group(
            id=id,
            user_id="1",
            name="Clay craft",
            description="All things related to clay"
        ).dict()


@router.post("/")
async def create(id: str, group: Group):
    return Response(status_code=201)

@router.put("/{id}")
async def update(id: str, group: Group):
    return Response(status_code=200)


@router.delete("/{id}")
async def delete(id: str):
    return Response(status_code=200)
