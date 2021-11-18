from fastapi import APIRouter, Response, Request, HTTPException, Depends
from sqlalchemy import exists
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from handsy.api import JWTBearer
from handsy.api.db.exceptions import SelectFailed
from handsy.api.models.group import GroupEntity
from handsy.api.models.item import Item, ItemEntity
from handsy.api.models.user import UserRole

router = APIRouter()


@router.get("/user/{user_id}/group/{group_id}/item")
async def get_all_user_group_items(user_id: str, group_id: str, req: Request):
    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )
    return {
        "value": [Item.from_orm(de) for de in
                  await ItemEntity.select(req.state.db, None, ItemEntity.group_id == group_id)]
    }


@router.get("/user/{user_id}/group/{group_id}/item/{item_id}")
async def get_user_group_item(user_id: str, group_id: str, item_id: str, req: Request):
    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )
    return {
        "value": Item.from_orm(await ItemEntity.select(req.state.db, item_id, ItemEntity.group_id == group_id))
    }


@router.post("/user/{user_id}/group/{group_id}/item", status_code=201, dependencies=[Depends(JWTBearer())])
async def create(user_id: str, group_id: str, item: Item, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != user_id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )

    session: Session = req.state.db
    q = exists(select(ItemEntity).filter(ItemEntity.name == item.name)).select()
    if (await session.execute(q)).scalar():
        raise HTTPException(400, f"Group with name {item.name} already exists")

    item.group_id = group_id
    item_id = await ItemEntity.create(req.state.db, item)
    return {
        "value": {
            "id": item_id
        }
    }


@router.put("/user/{user_id}/group/{group_id}/item/{item_id}", dependencies=[Depends(JWTBearer())])
async def update(user_id: str, group_id: str, item_id: str, item: Item, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != user_id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )

    try:
        item_entity = await ItemEntity.select(req.state.db, item_id, ItemEntity.group_id == group_id)
    except SelectFailed as ex:
        print("here")
        raise HTTPException(status_code=400, detail=str(ex))

    session: Session = req.state.db
    q = exists(select(ItemEntity).filter(ItemEntity.name == item.name)).select()
    if (await session.execute(q)).scalar():
        raise HTTPException(400, f"Group with name {item.name} already exists")

    item.group_id = group_id
    item.id = item_id
    await ItemEntity.update(req.state.db, item_id, item)
    return Response(status_code=200)


@router.delete("/user/{user_id}/group/{group_id}/item/{item_id}", dependencies=[Depends(JWTBearer())])
async def delete(user_id: str, group_id: str, item_id: str, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != user_id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )
    await ItemEntity.delete(req.state.db, item_id)
    return Response(status_code=204)
