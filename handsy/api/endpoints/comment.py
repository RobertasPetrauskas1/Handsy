from fastapi import APIRouter, Response, Request, HTTPException, Depends

from handsy.api import JWTBearer
from handsy.api.db.exceptions import SelectFailed
from handsy.api.models.comment import Comment, CommentEntity
from handsy.api.models.group import GroupEntity
from handsy.api.models.item import ItemEntity
from handsy.api.models.user import UserRole

router = APIRouter()


@router.get("/user/{user_id}/group/{group_id}/item/{item_id}/comment")
async def get_all_user_group_item_comments(user_id: str, group_id: str, item_id: str, req: Request):
    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )

    try:
        item_entity = await ItemEntity.select(req.state.db, item_id, ItemEntity.group_id == group_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"Group with id: {group_id} doesnt own item with id: {item_id}"
        )

    return {
        "value": [Comment.from_orm(de) for de in await CommentEntity.select(req.state.db, None, CommentEntity.item_id == item_id)]
    }


@router.get("/user/{user_id}/group/{group_id}/item/{item_id}/comment/{comment_id}")
async def get_user_group_item_comment(user_id: str, group_id: str, item_id: str, comment_id: str, req: Request):
    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )

    try:
        item_entity = await ItemEntity.select(req.state.db, item_id, ItemEntity.group_id == group_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"Group with id: {group_id} doesnt own item with id: {item_id}"
        )

    return {
        "value": Comment.from_orm(await CommentEntity.select(req.state.db, comment_id, CommentEntity.item_id == item_id))
    }


@router.post("/user/{user_id}/group/{group_id}/item/{item_id}/comment", status_code=201, dependencies=[Depends(JWTBearer())])
async def create(user_id: str, group_id: str, item_id: str, comment: Comment, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != user_id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    req_user_id = jwt_payload["uid"]
    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )

    try:
        item_entity = await ItemEntity.select(req.state.db, item_id, ItemEntity.group_id == group_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"Group with id: {group_id} doesnt own item with id: {item_id}"
        )

    comment.user_id = req_user_id
    comment.item_id = item_id
    comment_id = await CommentEntity.create(req.state.db, comment)

    return {
        "value": {
            "id": comment_id
        }
    }


@router.put("/user/{user_id}/group/{group_id}/item/{item_id}/comment/{comment_id}", dependencies=[Depends(JWTBearer())])
async def update(user_id: str, group_id: str, item_id: str, comment_id: str, comment: Comment, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != user_id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")

    req_user_id = jwt_payload["uid"]
    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )

    try:
        item_entity = await ItemEntity.select(req.state.db, item_id, ItemEntity.group_id == group_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"Group with id: {group_id} doesnt own item with id: {item_id}"
        )

    try:
        comment_entity = await CommentEntity.select(req.state.db, comment_id, CommentEntity.item_id == item_id)
    except SelectFailed as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    if comment_entity.user_id != req_user_id:
        raise HTTPException(status_code=400, detail=f"User with id: {req_user_id} doesnt own comment with id: {comment_id}")

    comment.user_id = comment_entity.user_id
    comment.timestamp = comment_entity.timestamp
    comment.item_id = comment_entity.item_id
    comment.id = comment_id
    await CommentEntity.update(req.state.db, comment_id, comment)
    return Response(status_code=200)


@router.delete("/user/{user_id}/group/{group_id}/item/{item_id}/comment/{comment_id}", dependencies=[Depends(JWTBearer())])
async def delete(user_id: str, group_id: str, item_id: str, comment_id: str, req: Request):
    jwt_payload = req.state.jwt_payload
    if jwt_payload["uid"] != user_id and jwt_payload["urole"] != UserRole.ADMIN:
        raise HTTPException(403, "Unauthorized")
    req_user_id = jwt_payload["uid"]

    try:
        group_entity = await GroupEntity.select(req.state.db, group_id, GroupEntity.user_id == user_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"User with id: {user_id} doesnt own group with id: {group_id}"
        )

    try:
        item_entity = await ItemEntity.select(req.state.db, item_id, ItemEntity.group_id == group_id)
    except SelectFailed:
        raise HTTPException(
            status_code=400,
            detail=f"Group with id: {group_id} doesnt own item with id: {item_id}"
        )

    await CommentEntity.delete(req.state.db, comment_id, CommentEntity.user_id == req_user_id)
    return Response(status_code=204)
