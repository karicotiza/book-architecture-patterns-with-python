"""SQL repository mock."""

from src.domain.entities.batch import Batch


class SQLRepositoryMock:
    """SQL repository mock."""

    def __init__(self, batches: list[Batch]) -> None:
        """Create new instance.

        Args:
            batches (list[Batch]): initial data.

        """
        self._batches = set(batches)

    def all(self) -> list[Batch]:
        """Get all batch entities from repository.

        Returns:
            list[Batch]: list of batch entities.

        """
        return list(self._batches)

    def get(self, reference: str) -> Batch:
        """Get batch entity from repository by reference.

        Args:
            reference (str): batch entity reference.

        Returns:
            Batch: batch entity

        """
        return next(
            batch for batch in self._batches if batch.reference == reference
        )

    def add(self, batch: Batch) -> None:
        """Add batch entity to repository.

        Args:
            batch (Batch): batch entity.

        """
        self._batches.add(batch)
