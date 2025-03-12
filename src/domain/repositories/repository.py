"""Database repository interface."""

from typing import Protocol

from src.domain.entities.batch import Batch


class IRepository(Protocol):
    """Database repository interface."""

    def add(self, batch: Batch) -> None:
        """Add batch entity to repository.

        Args:
            batch (Batch): batch entity.

        """
        ...

    def get(self, reference: str) -> Batch:
        """Get batch entity from repository by reference.

        Args:
            reference (str): batch entity reference.

        Returns:
            Batch: batch entity

        """
        ...
