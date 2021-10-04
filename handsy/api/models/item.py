from pydantic import BaseModel


class Item(BaseModel):
    id: str
    group_id: str
    name: str
    description: str
