from typing import Iterable

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from handsy.api.db.exceptions import DeleteFailed, SelectFailed, UpdateFailed


class Crud:
    id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    async def select(cls, session: Session, idx=None, *where):
        if idx and isinstance(idx, (str, int)):
            try:
                return (await session.execute(select(cls).where(cls.id == idx, *where))).scalar_one()
            except NoResultFound:
                raise SelectFailed(f"No {cls.__name__} with id: {idx}")

        elif idx and isinstance(idx, Iterable):
            return (await session.execute(select(cls).where(cls.id.in_(idx), *where))).scalars().all()
        elif idx:
            raise Exception("Unexpected type of id. Expected int or str")

        return (await session.execute(select(cls).where(*where))).scalars().all()

    @classmethod
    async def create(cls, session: Session, model: BaseModel):
        entity = cls(**model.dict())
        session.add(entity)
        await session.flush()
        return entity.id

    @classmethod
    async def update(cls, session: Session, idx: str, model: BaseModel, *where):
        statement = update(cls).where(cls.id == idx, *where).values(**model.dict())
        result = await session.execute(statement)
        if result.rowcount != 1:
            raise UpdateFailed(f"No {cls.__name__} with id: {idx}")

    @classmethod
    async def delete(cls, session: Session, idx: str, *where):
        try:
            # select is needed for using orm-like delete instead of executing a statement.
            # By using orm-like delete, deleting a entity also cascades the deletes to its many to many relationships
            entity = await cls.select(session, idx, *where)
            await session.delete(entity)
        except SelectFailed as ex:
            raise DeleteFailed(str(ex))

    async def add_to(self, session: Session):
        session.add(self)
        await session.flush()
        return self.id
