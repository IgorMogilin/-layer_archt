from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from app.application.ports import UnitOfWork
from app.infrastructure.db.session import async_session_maker
from app.infrastructure.db.uow import SqlAlchemyUnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with async_session_maker() as session:
        yield SqlAlchemyUnitOfWork(session)


UowDep = Annotated[UnitOfWork, Depends(get_uow)]