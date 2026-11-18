from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from app.domain.errors import EmptyOrder, InvalidStatusTransition


class OrderStatus(str, Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"


@dataclass(frozen=True)
class OrderItem:
    product_id: int
    qty: int
    price: Decimal


@dataclass
class Order:
    id: int | None
    customer_id: int
    items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.DRAFT

    @property
    def total(self) -> Decimal:
        return sum((i.qty * i.price for i in self.items), Decimal(0))

    def confirm(self) -> None:
        if not self.items:
            oid = self.id if self.id is not None else "<unsaved>"
            raise EmptyOrder(f"order {oid} has no items")
        if self.status is not OrderStatus.DRAFT:
            raise InvalidStatusTransition(f"{self.status.value} -> confirmed")
        self.status = OrderStatus.CONFIRMED