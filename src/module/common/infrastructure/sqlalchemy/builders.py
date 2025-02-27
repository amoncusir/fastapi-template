from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import DatabaseConfig


def build_sqlalchemy_engine(config: DatabaseConfig) -> AsyncEngine:
    return create_async_engine(
        url=config.url,
        pool_size=config.pool_size,
        echo=config.enable_echo,
    )


def build_sqlalchemy_session_maker(engine: AsyncEngine) -> Callable[[], AsyncSession]:
    return async_sessionmaker(engine)
