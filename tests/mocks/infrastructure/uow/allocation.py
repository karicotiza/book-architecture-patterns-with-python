"""Allocation unit of work mock."""

from types import TracebackType
from typing import Self

from src.domain.interfaces.repositories.sql_repository import SQLRepository
from tests.mocks.infrastructure.repositories.sql_repository import (
    SQLRepositoryMock,
)


class AllocationUOWMock:
    """Allocation unit of work."""

    def __init__(self) -> None:
        """Create new instance."""
        self._products: SQLRepositoryMock = SQLRepositoryMock([])
        self.committed: bool = False

    @property
    def products(self) -> SQLRepository:
        """Get products.

        Returns:
            SQLRepository: Products as SQL repository.

        """
        return self._products

    def commit(self) -> None:
        """Commit changes."""
        self.committed = True

    def rollback(self) -> None:
        """Rollback changes."""

    def close(self) -> None:
        """Close connection."""

    def __enter__(self) -> Self:
        """Enter dunder method."""
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
        self.close()
