from app.application.ports import UnitOfWork
from app.domain.errors import OrderNotFound
from app.domain.order import Order


class CancelOrder:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, order_id: int) -> Order:
        async with self._uow:
            order = await self._uow.orders.get(order_id)
            if order is None:
                raise OrderNotFound(f"order {order_id}")
            order.cancel()
            await self._uow.orders.save(order)
            await self._uow.commit()
            return order