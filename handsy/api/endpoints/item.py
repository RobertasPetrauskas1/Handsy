from fastapi import APIRouter, Response
from handsy.api.models.item import Item

router = APIRouter(prefix="/item")


@router.get("/")
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


@router.get("/{id}")
async def get(id: str):
    return Item(
            id=id,
            group_id="1",
            name="Pot1",
            description="my first clay pot"
        ).dict()


@router.post("/")
async def create(item: Item):
    return Response(status_code=201)


@router.put("/{id}")
async def update(id: str, item: Item):
    return Response(status_code=200)


@router.delete("/{id}")
async def delete(id: str):
    return Response(status_code=200)
