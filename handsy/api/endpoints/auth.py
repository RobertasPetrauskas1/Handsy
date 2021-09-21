from fastapi import APIRouter, Response

from handsy.api.models.auth import Credentials

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(credentials: Credentials):
    return Response(status_code=201)


@router.post("/login")
async def login(credentials: Credentials):
    return {"token": "some_jwt_token"}
