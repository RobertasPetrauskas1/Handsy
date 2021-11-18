from fastapi import APIRouter, Response, Request, HTTPException, Depends
from sqlalchemy import exists
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from handsy.api import JWTBearer
from handsy.api.db.exceptions import SelectFailed
from handsy.api.models.group import Group, GroupEntity
from handsy.api.models.user import UserRole

router = APIRouter()


@router.get("/user/{user_id}/group")
async def get_all_user_groups(user_id: str, req: Request):
    return {
        "value": [Group.from_orm(de) for de in await GroupEntity.select(req.state.db, None, GroupEntity.user_id == user_id)]
    }


@router.get("/user/{user_id}/group/{group_id}")
async def get_user_group(user_id: str, group_id: str, req: Request):
    return {
        "value": Group.from_orm(await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id))
    }


@router.get("/group")
async def get_all(req: Request):
    return {
        "value": [Group.from_orm(de) for de in await GroupEntity.select(req.state.db)]
    }


@router.post("/user/{user_id}/group", status_code=201, dependencies=[Depends(JWTBearer())])
async def create(user_id: str, group: Group, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != user_id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    session: Session = req.state.db
    q = exists(select(GroupEntity).filter(GroupEntity.name == group.name)).select()
    if (await session.execute(q)).scalar():
        raise HTTPException(400, f"Group with name {group.name} already exists")

    group.user_id = user_id
    group_id = await GroupEntity.create(req.state.db, group)
    return {
        "value": {
            "id": group_id
        }
    }


@router.put("/user/{user_id}/group/{group_id}", dependencies=[Depends(JWTBearer())])
async def update(user_id: str, group_id: str, group: Group, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != user_id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    try:
        entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    session: Session = req.state.db
    q = exists(select(GroupEntity).filter(GroupEntity.name == group.name)).select()
    if (await session.execute(q)).scalar():
        raise HTTPException(400, f"Group with name {group.name} already exists")

    group.user_id = user_id
    await GroupEntity.update(req.state.db, group_id, group)

    return Response(status_code=200)


@router.delete("/user/{user_id}/group/{group_id}", dependencies=[Depends(JWTBearer())])
async def delete(user_id: str, group_id: str, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != user_id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    await GroupEntity.delete(req.state.db, group_id, GroupEntity.user_id == user_id)
    return Response(status_code=204)
