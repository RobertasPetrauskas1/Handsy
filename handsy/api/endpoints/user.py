from fastapi import APIRouter, Response, Request, HTTPException, Depends

from handsy.api import JWTBearer
from handsy.api.db.exceptions import SelectFailed
from handsy.api.models.auth import CredentialsEntity
from handsy.api.models.user import User, UserEntity, UserRole

router = APIRouter(prefix="/user")


@router.get("/")
async def get_all(req: Request):
    return {
        "value": [User.from_orm(de) for de in await UserEntity.select(req.state.db)]
    }


@router.get("/{id}")
async def get(id: str, req: Request):
    return {
        "value": User.from_orm(await UserEntity.select(req.state.db, id))
    }


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update(id: str, user: User, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    try:
        entity = await UserEntity.select(req.state.db, id)
    except SelectFailed as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    user.id = id
    await UserEntity.update(req.state.db, id, user)

    return Response(status_code=200)


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete(id: str, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    credentials_id = (await UserEntity.select(req.state.db, id)).credentials.id

    await UserEntity.delete(req.state.db, id)
    await CredentialsEntity.delete(req.state.db, credentials_id)
    return Response(status_code=204)
