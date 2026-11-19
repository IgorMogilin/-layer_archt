from decimal import Decimal
from typing import Annotated, Self

from pydantic import BaseModel, Field, ConfigDict

from app.domain.order import Order, OrderStatus

ProductId = Annotated[int, Field(gt=0)]
CustomerId = Annotated[int, Field(gt=0)]
Qty = Annotated[int, Field(gt=0, le=1000)]
Money = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]


class OrderItemIn(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    product_id: ProductId
    qty: Qty
    price: Money


class OrderIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: CustomerId
    items: Annotated[list[OrderItemIn], Field(min_length=1)]


class OrderOut(BaseModel):
    id: int
    customer_id: CustomerId
    status: OrderStatus
    total: Money

    @classmethod
    def from_domain(cls, order: Order) -> Self:
        if order.id is None:
            raise ValueError("cannot serialize unsaved order")
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status,
            total=order.total,
        )