from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports import OrderRepository
from app.infrastructure.db.order_repository import SqlAlchemyOrderRepository


class SqlAlchemyUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session
        self.orders: OrderRepository = SqlAlchemyOrderRepository(session)

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        if exc_info[0] is not None:
            await self.rollback()

    async def commit(self) -> None:
        await self._s.commit()

    async def rollback(self) -> None:
        await self._s.rollback()