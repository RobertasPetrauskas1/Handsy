from pydantic import BaseModel
from handsy.api.models.group import Group


class Item(BaseModel):
    id: str
    group_id: str
    name: str
    description: str
