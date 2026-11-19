from fastapi import APIRouter

from app.api.deps import UowDep
from app.api.error_handlers import PROBLEM
from app.api.schemas import OrderIn, OrderOut
from app.application.use_cases.cancel_order import CancelOrder
from app.application.use_cases.confirm_order import ConfirmOrder
from app.application.use_cases.create_order import CreateOrder

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post(
    "",
    response_model=OrderOut,
    status_code=201,
    responses={422: PROBLEM},
    summary="Создать заказ",
    operation_id="createOrder",
)
async def create_order(
    payload: OrderIn,
    uow: UowDep,
) -> OrderOut:
    order = await CreateOrder(uow).execute(
        customer_id=payload.customer_id,
        items=[(i.product_id, i.qty, i.price) for i in payload.items],
    )
    return OrderOut.from_domain(order)


@router.post(
    "/{order_id}/confirm",
    response_model=OrderOut,
    responses={
        404: PROBLEM,
        409: PROBLEM | {"description": "invalid-status-transition"},
        422: PROBLEM,
    },
    summary="Подтвердить заказ",
    operation_id="confirmOrder",
)
async def confirm_order(
    order_id: int,
    uow: UowDep,
) -> OrderOut:
    order = await ConfirmOrder(uow).execute(order_id)
    return OrderOut.from_domain(order)


@router.post(
    "/{order_id}/cancel",
    response_model=OrderOut,
    responses={
        404: PROBLEM,
        409: PROBLEM
        | {
            "description": (
                "order-already-cancelled — заказ уже отменён; "
                "invalid-status-transition — отмена разрешена только из draft"
            )
        },
    },
    summary="Отменить заказ",
    operation_id="cancelOrder",
)
async def cancel_order(
        order_id: int,
        uow: UowDep,
) -> OrderOut:
    order = await CancelOrder(uow).execute(order_id)
    return OrderOut.from_domain(order)