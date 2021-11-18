import datetime
import re
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel, validator, Field
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from handsy.api.db import DbBase
from handsy.api.db.crud import Crud


class Registration(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    birth_date: str
    description: Optional[str] = Field(None, max_length=300)
    email: str
    password: str = Field(..., min_length=5)

    class Config:
        orm_mode = True

    @validator('birth_date')
    def must_be_valid_date(cls, v):
        try:
            datetime.datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise HTTPException(400, "Incorrect birth_date. Must be of format YYYY-MM-DD")

    @validator("email")
    def must_be_valid_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise HTTPException(400, "Invalid email format.")
        return v


class Credentials(BaseModel):
    email: str
    password: str


class CredentialsEntity(DbBase, Crud):
    __tablename__ = "credentials"
    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid4()))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("user.id"))
    user = relationship("UserEntity", back_populates="credentials", uselist=False, lazy="selectin")
