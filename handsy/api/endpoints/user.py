from fastapi import APIRouter, Response

from handsy.api.models.user import User

router = APIRouter(prefix="/user")


@router.get("/")
async def get_all():
    return [
        User(id="1", first_name="Name1", last_name="Surname1", birth_date="1999-01-01", description="Hi!").dict(),
        User(id="2", first_name="Name2", last_name="Surname2", birth_date="1999-01-01", description="Hi!").dict()
    ]


@router.get("/{id}")
async def get(id: str):
    return User(id=id, first_name="Name1", last_name="Surname1", birth_date="1999-01-01", description="Hi!").dict()


@router.put("/{id}")
async def update(id: str, user: User):
    return Response(status_code=200)


@router.delete("/{id}")
async def delete(id: str):
    return Response(status_code=200)
