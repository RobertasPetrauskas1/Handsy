from pydantic import BaseModel
from handsy.api.models.user import User


class Comment(BaseModel):
    id: str
    item_id: str
    user_id: User
    message: str
