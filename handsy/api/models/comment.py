import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from handsy.api.db import DbBase
from handsy.api.db.crud import Crud


class Comment(BaseModel):
    id: Optional[str]
    timestamp: Optional[datetime.datetime]
    item_id: Optional[str]
    user_id: Optional[str]
    message: str = Field(..., max_length=300)

    class Config:
        orm_mode = True


class CommentEntity(DbBase, Crud):
    __tablename__ = "comment"
    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid4()))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    item_id = Column(String, ForeignKey("item.id"))
    user_id = Column(String, ForeignKey("user.id"))
    message = Column(String, nullable=False)
    item = relationship("ItemEntity", back_populates="comments", lazy="selectin")
