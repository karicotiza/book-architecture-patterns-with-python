"""Allocation domain service."""

from src.domain.entities.batch import Batch
from src.domain.exceptions.out_of_stock import OutOfStockError
from src.domain.value_objects.order_line import OrderLine


class AllocationService:
    """Allocation domain service."""

    def allocate(self, order_line: OrderLine, batches: list[Batch]) -> str:
        """Allocate order line.

        Args:
            order_line (OrderLine): order line value objects.
            batches (list[OrderLine]): list of batch entities.

        Returns:
            str: allocated batch reference attribute.

        """
        try:
            batch: Batch = self._get_batch(order_line, batches)
        except StopIteration:
            msg: str = f"There is no {order_line.stock_keeping_unit} left"
            raise OutOfStockError(msg) from StopIteration

        batch.allocate(order_line)

        return batch.reference

    def _get_batch(self, order_line: OrderLine, batches: list[Batch]) -> Batch:
        return next(
            batch
            for batch in sorted(batches)
            if batch.can_allocate(order_line)
        )
