from fastapi import APIRouter, Response
from handsy.api.models.item import Item

router = APIRouter()


@router.get("/user/{user_id}/group/{group_id}/item")
async def get_all_user_group_items(user_id, group_id):
    return [
        Item(
            id="1",
            group_id=group_id,
            name="Pot1",
            description="my first clay pot"
        ).dict(),
        Item(
            id="2",
            group_id=group_id,
            name="Broken pot",
            description="sadly I broke Pot1"
        ).dict()
    ]


@router.get("/user/{user_id}/group/{group_id}/item/{item_id}")
async def get_user_group_item(user_id, group_id, item_id):
    return Item(
        id=item_id,
        group_id=group_id,
        name="Pot1",
        description="my first clay pot"
    ).dict()


@router.get("/item")
async def get_all():
    return [
        Item(
            id="1",
            group_id="1",
            name="Pot1",
            description="my first clay pot"
        ).dict(),
        Item(
            id="2",
            group_id="1",
            name="Broken pot",
            description="sadly I broke Pot1"
        ).dict()
    ]


@router.get("/item/{id}")
async def get(id: str):
    return Item(
        id=id,
        group_id="1",
        name="Pot1",
        description="my first clay pot"
    ).dict()


@router.post("/item")
async def create(item: Item):
    return Response(status_code=201)


@router.put("/item/{id}")
async def update(id: str, item: Item):
    return Response(status_code=200)


@router.delete("/item/{id}")
async def delete(id: str):
    return Response(status_code=204)
