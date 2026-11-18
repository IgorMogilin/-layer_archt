from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.errors import EmptyOrder, InvalidStatusTransition, OrderNotFound

STATUS_MAP: dict[type[Exception], int] = {
    OrderNotFound: 404,
    EmptyOrder: 422,
    InvalidStatusTransition: 409,
}


async def domain_error_handler(request: Request, exc: Exception) -> JSONResponse:
    status = STATUS_MAP.get(type(exc), 400)
    return JSONResponse(
        status_code=status,
        content={
            "type": "about:blank",
            "title": type(exc).__name__,
            "status": status,
            "detail": str(exc),
            "instance": str(request.url),
        },
        media_type="application/problem+json",
    )