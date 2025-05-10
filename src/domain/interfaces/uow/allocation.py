"""Allocation unit of work interface."""

from types import TracebackType
from typing import Protocol, Self

from src.domain.interfaces.repositories.sql_repository import SQLRepository


class AllocationUOW(Protocol):
    """Allocation unit of work."""

    @property
    def products(self) -> SQLRepository:
        """Get products.

        Returns:
            SQLRepository: Products as SQL repository.

        """
        ...

    def commit(self) -> None:
        """Commit changes."""
        ...

    def rollback(self) -> None:
        """Rollback changes."""
        ...

    def __enter__(self) -> Self:
        """Enter dunder method."""
        ...

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
        ...
