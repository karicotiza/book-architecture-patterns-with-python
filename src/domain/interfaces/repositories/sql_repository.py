"""SQL repository interface."""

from typing import Protocol

from src.domain.entities.batch import Batch


class SQLRepository(Protocol):
    """SQL repository interface."""

    def all(self) -> list[Batch]:
        """Get all batch entities from repository.

        Returns:
            list[Batch]: all batch entities

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

    def add(self, batch: Batch) -> None:
        """Add batch entity to repository.

        Args:
            batch (Batch): batch entity.

        """
        ...
