"""PostgreSQL allocation unit of work."""

from collections.abc import Callable
from types import TracebackType
from typing import Self

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.repositories.sql_repository.postgresql import (
    PostgreSQLRepository,
)
from src.infrastructure.settings import settings

default_session_factory: sessionmaker = sessionmaker(
    bind=create_engine(settings.postgres_uri),
)


class PostgresqlAllocationUOW:
    """PostgreSQL allocation unit of work."""

    _msg: str = (
        "First, you should enter the context. "
        "E. g. with PostgresqlAllocationUOW():```"
    )

    def __init__(
        self,
        session_factory: Callable[[], Session] = default_session_factory,
    ) -> None:
        """Create new instance.

        Args:
            session_factory (Callable[[], Session]): SQLAlchemy's session
                factory.

        """
        self._session_factory: Callable[[], Session] = session_factory
        self._session: Session | None = None

    @property
    def session(self) -> Session:
        """Get session.

        Returns:
            Session: SQLAlchemy's session.

        """
        if self._session:
            return self._session

        raise ValueError(self._msg)

    @property
    def products(self) -> PostgreSQLRepository:
        """Get products.

        Returns:
            SQLRepository: products as SQL repository.

        """
        if self._session:
            return self._sql_repository

        raise ValueError(self._msg)

    def commit(self) -> None:
        """Commit changes."""
        if self._session:
            self._session.commit()
        else:
            raise ValueError(self._msg)

    def rollback(self) -> None:
        """Rollback changes."""
        if self._session:
            self._session.rollback()
        else:
            raise ValueError(self._msg)

    def __enter__(self) -> Self:
        """Enter dunder method."""
        self._session = self._session_factory()
        self._sql_repository: PostgreSQLRepository = PostgreSQLRepository(
            session=self._session,
        )

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit dunder method.

        Args:
            exc_type (type[BaseException] | None): exception type.
            exc_val (BaseException | None): exception value.
            exc_tb (TracebackType | None): exception traceback.

        """
        self.rollback()

        if self._session:
            self._session.close()
