from decimal import Decimal

from pydantic import BaseModel, Field

from app.domain.order import Order


class OrderItemIn(BaseModel):
    product_id: int
    qty: int = Field(gt=0)
    price: Decimal = Field(gt=0)


class OrderIn(BaseModel):
    customer_id: int
    items: list[OrderItemIn]


class OrderOut(BaseModel):
    id: int
    customer_id: int
    status: str
    total: Decimal

    @classmethod
    def from_domain(cls, order: Order) -> "OrderOut":
        if order.id is None:
            raise ValueError("cannot serialize unsaved order")
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status.value,
            total=order.total,
        )