from fastapi import APIRouter, Depends

from app.api.deps import get_uow
from app.api.schemas import OrderIn, OrderOut
from app.application.ports import UnitOfWork
from app.application.use_cases.cancel_order import CancelOrder
from app.application.use_cases.confirm_order import ConfirmOrder
from app.application.use_cases.create_order import CreateOrder

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
async def create_order(
    payload: OrderIn,
    uow: UnitOfWork = Depends(get_uow),
) -> OrderOut:
    order = await CreateOrder(uow).execute(
        customer_id=payload.customer_id,
        items=[(i.product_id, i.qty, i.price) for i in payload.items],
    )
    return OrderOut.from_domain(order)


@router.post("/{order_id}/confirm", response_model=OrderOut)
async def confirm_order(
    order_id: int,
    uow: UnitOfWork = Depends(get_uow),
) -> OrderOut:
    order = await ConfirmOrder(uow).execute(order_id)
    return OrderOut.from_domain(order)


@router.post("/{order_id}/cancel", response_model=OrderOut)
async def cancel_order(
        order_id: int,
        uow: UnitOfWork = Depends(get_uow),
) -> OrderOut:
    order = await CancelOrder(uow).execute(order_id)
    return OrderOut.from_domain(order)