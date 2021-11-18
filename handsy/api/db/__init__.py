from contextlib import asynccontextmanager
from typing import Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

import handsy

_db_engine: Optional[Engine] = None
_session_type: Optional[Type[Session]]

DbBase = declarative_base()
# import models for alembic migrations
from handsy.api.models import *


async def create_db_engine():
    settings = handsy.get_settings()
    global _db_engine
    _db_engine = create_async_engine(settings.handsy_database_url, echo=settings.sql_echo)
    global _session_type
    _session_type = sessionmaker(bind=_db_engine, future=True, class_=AsyncSession)


async def dispose_db_engine():
    global _session_type
    _session_type = None

    global _db_engine
    if _db_engine:
        await _db_engine.dispose()
        _db_engine = None


@asynccontextmanager
async def db_session_manager():
    global _session_type
    session = _session_type()
    try:
        yield session
        await session.commit()
    finally:
        await session.close()
