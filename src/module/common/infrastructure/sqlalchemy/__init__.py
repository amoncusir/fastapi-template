from contextlib import AbstractAsyncContextManager
from typing import Protocol

from .container import SqlAlchemyAsyncContainer


class UnitOfWork(Protocol):

    async def __call__(
        self, transaction: bool = None
    ) -> AbstractAsyncContextManager: ...


__all__ = ["SqlAlchemyAsyncContainer", "UnitOfWork"]
