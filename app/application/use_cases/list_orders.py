from dataclasses import dataclass

from app.application.ports import UnitOfWork
from app.domain.order import Order, OrderStatus


@dataclass(frozen=True)
class OrdersPage:
    items: list[Order]
    total: int


class ListOrders:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        *,
        limit: int,
        offset: int,
        ascending: bool,
        status: OrderStatus | None,
    ) -> OrdersPage:
        async with self._uow:
            items = await self._uow.orders.list(
                limit=limit, offset=offset, ascending=ascending, status=status
            )
            total = await self._uow.orders.count(status=status)
            return OrdersPage(items=items, total=total)