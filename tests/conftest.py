"""Pytest configuration."""

from collections.abc import Generator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from src.infrastructure.repositories.sql_repository.postgresql import (
    create_mappers,
    metadata,
)
from src.infrastructure.settings import settings
from tests.utils.sql_database_filler import SQLRepositoryFiller


@pytest.fixture
def in_memory_db() -> Engine:
    """In memory DB fixture."""
    engine: Engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)

    return engine


@pytest.fixture
def session_factory(
    in_memory_db: Engine,
) -> Generator[sessionmaker, None, None]:
    """Session factory fixture.

    Args:
        in_memory_db (Engine): Engine.

    Yields:
        Generator[Session, None, None]: session factory.

    """
    create_mappers()

    yield sessionmaker(bind=in_memory_db)

    clear_mappers()


@pytest.fixture
def session(in_memory_db: Engine) -> Generator[Session, None, None]:
    """In memory DB session fixture.

    Args:
        in_memory_db (Engine): in memory db engine.

    Yields:
        Generator[Session, None, None]: in memory db session.

    """
    create_mappers()

    yield sessionmaker(bind=in_memory_db)()

    clear_mappers()


@pytest.fixture
def sqlalchemy_mapping() -> Generator[bool, None, None]:
    """SQLAlchemy mapping fixture."""
    create_mappers()

    yield True

    clear_mappers()


@pytest.fixture(scope="session")
def postgres_db() -> Engine:
    """PostgreSQL fixture."""
    engine: Engine = create_engine(settings.postgres_uri)
    metadata.create_all(engine)

    return engine


@pytest.fixture
def postgres_session(postgres_db: Engine) -> Generator[Session, None, None]:
    """PostgreSQL session fixture.

    Args:
        postgres_db (Engine): PostgreSQL engine.

    Yields:
        Generator[Session, None, None]: PostgreSQL session.

    """
    create_mappers()

    yield sessionmaker(bind=postgres_db)()

    clear_mappers()


@pytest.fixture
def sql_repository_filler(
    postgres_session: Session,
) -> Generator[SQLRepositoryFiller, None, None]:
    """SQLRepositoryFiller fixture.

    Args:
        postgres_session (Session): _description_

    Yields:
        Generator[SQLRepositoryFixture, None, None]: SQL repository fixture
            class.

    """
    sql_repository_fixture: SQLRepositoryFiller = SQLRepositoryFiller(
        session=postgres_session,
    )

    yield sql_repository_fixture

    sql_repository_fixture.delete_batches()
