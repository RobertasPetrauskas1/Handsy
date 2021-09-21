from fastapi import APIRouter, Response
from handsy.api.models.comment import Comment

router = APIRouter(prefix="/comment")


@router.get("/")
async def get_all():
    return [
        Comment(id="1", item_id="1", user_id="1", message="nice!").dict(),
        Comment(id="2", item_id="2", user_id="1", message="wow! great!").dict()
    ]


@router.get("/{id}")
async def get(id: str):
    return Comment(id="1", item_id="1", user_id="1", message="nice!").dict()


@router.post("/")
async def create(item: Comment):
    return Response(status_code=201)


@router.put("/{id}")
async def update(id: str, item: Comment):
    return Response(status_code=200)


@router.delete("/{id}")
async def delete(id: str):
    return Response(status_code=200)
