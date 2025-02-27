import threading
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession


class InvalidUnitOfWorkState(Exception):
    pass


class UnitOfWorkFactory:

    def __init__(self, session: AsyncSession):
        self.session = session

        self._locker = threading.Lock()
        self._deep = 0
        self._finished = False

    def _is_finished(self):
        with self._locker:
            return self._finished

    def _set_finished(self):
        with self._locker:
            self._finished = True

    def _add_deep(self):
        with self._locker:
            self._deep += 1

    def _sub_deep(self):
        with self._locker:
            self._deep -= 1

    def _reset_deep(self):
        with self._locker:
            self._deep = 0

    def _get_deep(self):
        with self._locker:
            return self._deep

    @asynccontextmanager
    async def __call__(self, transactional: bool = False):

        if self._is_finished():
            raise InvalidUnitOfWorkState("UnitOfWork already finished")

        self._add_deep()

        try:
            if transactional:
                if self.session.in_transaction():
                    await self.session.begin_nested()
                else:
                    await self.session.begin()

            yield

            await self.session.commit()
        except Exception:
            await self.session.rollback()
            self._reset_deep()

            raise
        finally:
            self._sub_deep()

            if self._get_deep() == 0:
                await self.session.close()
                self._set_finished()
