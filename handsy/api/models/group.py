from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from handsy.api.db import DbBase
from handsy.api.db.crud import Crud


class Group(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    name: str = Field(..., min_length=2)
    description: str = Field(..., max_length=300)

    class Config:
        orm_mode = True


class GroupEntity(DbBase, Crud):
    __tablename__ = "group"
    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid4()))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(String, ForeignKey("user.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    items = relationship("ItemEntity", back_populates="group", lazy="selectin")
    user = relationship("UserEntity", back_populates="groups", lazy="selectin")


