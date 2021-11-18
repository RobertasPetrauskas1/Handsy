from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from handsy.api.db import DbBase
from handsy.api.db.crud import Crud


class Item(BaseModel):
    id: Optional[str]
    group_id: Optional[str]
    name: str = Field(..., min_length=2)
    description: str = Field(..., max_length=300)

    class Config:
        orm_mode = True


class ItemEntity(DbBase, Crud):
    __tablename__ = "item"
    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid4()))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    group_id = Column(String, ForeignKey("group.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    group = relationship("GroupEntity", back_populates="items", lazy="selectin")
    comments = relationship("CommentEntity", back_populates="item", lazy="selectin")

