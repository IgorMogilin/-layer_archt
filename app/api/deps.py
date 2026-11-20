from collections.abc import AsyncGenerator
from typing import Annotated, Literal

from fastapi import Depends, Query
from pydantic import BaseModel, Field

from app.application.ports import UnitOfWork
from app.infrastructure.db.session import async_session_maker
from app.infrastructure.db.uow import SqlAlchemyUnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with async_session_maker() as session:
        yield SqlAlchemyUnitOfWork(session)


class PageParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    sort_order: Literal["asc", "desc"] = "desc"

    @property
    def ascending(self) -> bool:
        return self.sort_order == "desc"


Page = Annotated[PageParams, Query()]
UowDep = Annotated[UnitOfWork, Depends(get_uow)]