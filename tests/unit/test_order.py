from decimal import Decimal

import pytest

from app.domain.errors import (
    EmptyOrder,
    InvalidStatusTransition,
    OrderAlreadyCancelled,
)
from app.domain.order import Order, OrderItem, OrderStatus


def make_order(
    *,
    items: list[OrderItem] | None = None,
    status: OrderStatus = OrderStatus.DRAFT,
) -> Order:
    return Order(
        id=1,
        customer_id=1,
        items=items
        if items is not None
        else [OrderItem(product_id=1, qty=2, price=Decimal("100.00"))],
        status=status,
    )


def test_total_sums_items():
    order = make_order(
        items=[
            OrderItem(product_id=1, qty=2, price=Decimal("100.00")),
            OrderItem(product_id=2, qty=1, price=Decimal("50.00")),
        ]
    )
    assert order.total == Decimal("250.00")


def test_confirm_draft_with_items():
    order = make_order()
    order.confirm()
    assert order.status is OrderStatus.CONFIRMED


def test_confirm_empty_order_raises():
    order = make_order(items=[])
    with pytest.raises(EmptyOrder):
        order.confirm()
    assert order.status is OrderStatus.DRAFT


def test_confirm_twice_raises():
    order = make_order(status=OrderStatus.CONFIRMED)
    with pytest.raises(InvalidStatusTransition):
        order.confirm()


def test_cancel_draft():
    order = make_order()
    order.cancel()
    assert order.status is OrderStatus.CANCELLED


def test_cancel_twice_raises():
    order = make_order(status=OrderStatus.CANCELLED)
    with pytest.raises(OrderAlreadyCancelled):
        order.cancel()


def test_cancel_confirmed_raises():
    order = make_order(status=OrderStatus.CONFIRMED)
    with pytest.raises(InvalidStatusTransition):
        order.cancel()