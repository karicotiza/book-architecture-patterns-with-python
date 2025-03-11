"""Allocation domain service."""

from src.domain.entities.batch import Batch
from src.domain.value_objects.order_line import OrderLine


class AllocationService:
    """Allocation domain service."""

    def allocate(self, line: OrderLine, batches: list[Batch]) -> str:
        """Allocate order line.

        Args:
            line (OrderLine): order line value objects.
            batches (list[OrderLine]): list of batch entities.

        Returns:
            str: allocated batch reference attribute.

        """
        batch: Batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(line)
        )

        batch.allocate(line)

        return batch.reference
