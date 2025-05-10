"""Allocation application service."""

from typing import TYPE_CHECKING

from src.domain.entities.batch import Batch
from src.domain.value_objects.order_line import OrderLine
from src.infrastructure.uow.allocation.postgresql_allocation import (
    PostgresqlAllocationUOW,
)

if TYPE_CHECKING:
    from src.domain.aggregates.product import Product


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
            product: Product | None = unit_of_work.products.get(
                stock_keeping_unit=stock_keeping_unit,
            )

            if product is None:
                msg: str = f"Invalid SKU: {order_line.stock_keeping_unit}"
                raise InvalidSKUError(msg)

            batch_reference: str = product.allocate(order_line)

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
