from typing import Any, cast

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.domain.errors import (
    DomainError,
    EmptyOrder,
    InvalidStatusTransition,
    OrderAlreadyCancelled,
    OrderNotFound,
)

PROBLEM_JSON = "application/problem+json"
ERROR_BASE = "https://errors.layer-archt.local"


class ProblemDetail(BaseModel):
    """Schema-only модель: форма ошибки для OpenAPI, в рантайме не создаётся."""

    type: str = "about:blank"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None


# готовое описание для responses в роутерах
PROBLEM: dict[str, Any] = {"model": ProblemDetail, "content": {PROBLEM_JSON: {}}}


# класс ошибки -> (HTTP-статус, slug, title)
ERRORS: dict[type, tuple[int, str, str]] = {
    OrderNotFound: (404, "order-not-found", "Order not found"),
    EmptyOrder: (422, "empty-order", "Empty order"),
    InvalidStatusTransition: (
        409,
        "invalid-status-transition",
        "Invalid status transition",
    ),
    OrderAlreadyCancelled: (
        409,
        "order-already-cancelled",
        "Order already cancelled",
    ),
}

_DEFAULT: tuple[int, str, str] = (400, "domain-error", "Business rule violated")


def _resolve(exc: DomainError) -> tuple[int, str, str]:
    """Ищем запись по MRO: сначала конкретный тип, затем базовые."""
    for cls in type(exc).__mro__:
        if cls in ERRORS:
            return ERRORS[cls]
    return _DEFAULT


def problem(
    request: Request,
    status: int,
    slug: str,
    title: str,
    detail: str,
    **extensions: object,
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type=PROBLEM_JSON,
        content={
            "type": f"{ERROR_BASE}/{slug}",
            "title": title,
            "status": status,
            "detail": detail,
            "instance": request.url.path,
            **extensions,
        },
    )


async def domain_error_handler(request: Request, exc: Exception) -> JSONResponse:
    domain_exc = cast(DomainError, exc)
    status, slug, title = _resolve(domain_exc)
    return problem(request, status, slug, title, str(domain_exc))


async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    validation_exc = cast(RequestValidationError, exc)
    return problem(
        request,
        422,
        "validation-error",
        "Request validation failed",
        "One or more fields are invalid",
        errors=[
            {"loc": list(e["loc"]), "msg": e["msg"], "type": e["type"]}
            for e in validation_exc.errors()
        ],
    )