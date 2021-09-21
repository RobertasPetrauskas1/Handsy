from pydantic import BaseModel


class Group(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
