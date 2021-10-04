from fastapi import APIRouter, Response
from handsy.api.models.comment import Comment

router = APIRouter()


@router.get("/user/{user_id}/group/{group_id}/item/{item_id}/comment")
async def get_all_user_group_item_comments(user_id, group_id, item_id):
    return [
        Comment(id="1", item_id=item_id, user_id=user_id, message="nice!").dict(),
        Comment(id="2", item_id=item_id, user_id=user_id, message="wow! great!").dict()
    ]


@router.get("/user/{user_id}/group/{group_id}/item/{item_id}/comment/{comment_id}")
async def get_user_group_item_comment(user_id, group_id, item_id, comment_id):
    return Comment(id=comment_id, item_id=item_id, user_id=user_id, message="nice!").dict()


@router.get("/comment")
async def get_all():
    return [
        Comment(id="1", item_id="1", user_id="1", message="nice!").dict(),
        Comment(id="2", item_id="2", user_id="1", message="wow! great!").dict()
    ]


@router.get("/comment/{id}")
async def get(id: str):
    return Comment(id="1", item_id="1", user_id="1", message="nice!").dict()


@router.post("/comment")
async def create(item: Comment):
    return Response(status_code=201)


@router.put("/comment/{id}")
async def update(id: str, item: Comment):
    return Response(status_code=200)


@router.delete("/comment/{id}")
async def delete(id: str):
    return Response(status_code=204)
