from pydantic import BaseModel


class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    birth_date: str
    description: str
