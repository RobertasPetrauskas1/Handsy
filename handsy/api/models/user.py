import enum
from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel, validator, Field
from sqlalchemy import Column, String, func, DateTime, Enum
from sqlalchemy.orm import relationship

from handsy.api.db import DbBase
from handsy.api.db.crud import Crud


class User(BaseModel):
    id: Optional[str]
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    birth_date: str
    description: Optional[str] = Field(None, max_length=300)

    class Config:
        orm_mode = True

    @validator('birth_date')
    def must_be_valid_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise HTTPException(400, "Incorrect birth_date. Must be of format YYYY-MM-DD")


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class UserEntity(DbBase, Crud):
    __tablename__ = "user"
    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid4()))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    description = Column(String, nullable=False)
    credentials = relationship("CredentialsEntity", back_populates="user", uselist=False, lazy="selectin")
    groups = relationship("GroupEntity", back_populates="user", lazy="selectin")
    role = Column(Enum("ADMIN", "USER", name="UserRole"), nullable=False, default=UserRole.USER)
