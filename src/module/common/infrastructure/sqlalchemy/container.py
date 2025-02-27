from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.module.providers import ApplicationScoped, RequestScoped

from .builders import build_sqlalchemy_engine, build_sqlalchemy_session_maker
from .config import DatabaseConfig
from .unit_of_work import UnitOfWorkFactory


class SqlAlchemyAsyncContainer(DeclarativeContainer):
    config = providers.Configuration()

    database_config = ApplicationScoped(
        DatabaseConfig.from_dict,
        config=config,
    )

    engine = ApplicationScoped(
        build_sqlalchemy_engine,
        config=database_config,
    )

    session_maker = ApplicationScoped(
        build_sqlalchemy_session_maker,
        engine=engine,
    )

    session = RequestScoped(session_maker.provided.call())

    unit_of_work = RequestScoped(
        UnitOfWorkFactory,
        session,
    )
