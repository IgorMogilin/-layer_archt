from decimal import Decimal

from app.application.ports import UnitOfWork
from app.domain.order import Order, OrderItem


class CreateOrder:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        customer_id: int,
        items: list[tuple[int, int, Decimal]],
    ) -> Order:
        order = Order(
            id=None,
            customer_id=customer_id,
            items=[OrderItem(product_id=p, qty=q, price=pr) for p, q, pr in items],
        )
        async with self._uow:
            saved = await self._uow.orders.add(order)
            await self._uow.commit()
            return saved