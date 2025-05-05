"""Allocation application service."""

from src.domain.entities.batch import Batch
from src.domain.services.allocate import AllocationService
from src.domain.value_objects.order_line import OrderLine
from src.infrastructure.uow.allocation.postgresql_allocation import (
    PostgresqlAllocationUOW,
)


class InvalidSKUError(Exception):
    """Invalid stock keeping unit exception."""


class AllocationAppService:
    """Allocation application service."""

    def allocate(
        self,
        order_id: str,
        stock_keeping_unit: str,
        quantity: int,
        unit_of_work: PostgresqlAllocationUOW,
    ) -> str:
        """Process allocation."""
        order_line: OrderLine = OrderLine(
            order_id=order_id,
            stock_keeping_unit=stock_keeping_unit,
            quantity=quantity,
        )

        with unit_of_work:
            batches: list[Batch] = unit_of_work.batches.all()

            if not self._is_valid_sku(order_line.stock_keeping_unit, batches):
                msg: str = f"Invalid SKU: {order_line.stock_keeping_unit}"
                raise InvalidSKUError(msg)

            batch_reference = AllocationService().allocate(
                order_line=order_line,
                batches=batches,
            )

            unit_of_work.commit()

        return batch_reference

    def _is_valid_sku(
        self,
        stock_keeping_unit: str,
        batches: list[Batch],
    ) -> bool:
        return stock_keeping_unit in {
            batch.stock_keeping_unit for batch in batches
        }
