class DomainError(Exception):
    """База всех бизнес-ошибок домена. Не знает про HTTP."""


class OrderNotFound(DomainError):
    pass


class EmptyOrder(DomainError):
    pass


class InvalidStatusTransition(DomainError):
    pass