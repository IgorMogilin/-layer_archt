from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.order import Order, OrderItem, OrderStatus
from app.infrastructure.db.models import OrderItemRow, OrderRow


class SqlAlchemyOrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, order_id: int) -> Order | None:
        row = await self._s.get(OrderRow, order_id)
        return self._to_domain(row) if row else None

    async def add(self, order: Order) -> Order:
        row = OrderRow(
            customer_id=order.customer_id,
            status=order.status.value,
            items=[
                OrderItemRow(product_id=i.product_id, qty=i.qty, price=i.price)
                for i in order.items
            ],
        )
        self._s.add(row)
        await self._s.flush()
        return self._to_domain(row)

    async def save(self, order: Order) -> None:
        row = await self._s.get(OrderRow, order.id)
        if row is None:
            oid = order.id if order.id is not None else "<unsaved>"
            raise RuntimeError(f"order {oid} not found")
        row.status = order.status.value

    @staticmethod
    def _to_domain(row: OrderRow) -> Order:
        return Order(
            id=row.id,
            customer_id=row.customer_id,
            items=[
                OrderItem(product_id=i.product_id, qty=i.qty, price=i.price)
                for i in row.items
            ],
            status=OrderStatus(row.status),
        )