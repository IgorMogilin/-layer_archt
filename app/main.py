from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.error_handlers import domain_error_handler, validation_error_handler
from app.api.routers.orders import router as orders_router
from app.domain.errors import DomainError

app = FastAPI()
app.include_router(orders_router)
app.add_exception_handler(DomainError, domain_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)