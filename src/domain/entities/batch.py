"""BatchEntity."""

from datetime import date
from typing import Self

from src.domain.value_objects.order_line import OrderLine


class Batch:
    """Batch entity."""

    def __init__(
        self,
        reference: str,
        stock_keeping_unit: str,
        quantity: int,
        estimated_arrival_time: date | None,
    ) -> None:
        """Create new instance.

        Args:
            reference (str): order reference.
            stock_keeping_unit (str): stock keeping unit.
            quantity (int): quantity.
            estimated_arrival_time (date | None): estimated arrival time.

        """
        self.reference: str = reference
        self.stock_keeping_unit: str = stock_keeping_unit
        self.estimated_arrival_time: date | None = estimated_arrival_time
        self._purchased_quantity: int = quantity
        self._allocations: set[OrderLine] = set()

    def allocate(self, line: OrderLine) -> None:
        """Allocate order line.

        Args:
            line (OrderLine): order line value object.

        """
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        """Deallocate order line.

        Args:
            line (OrderLine): order line value object.

        """
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine) -> bool:
        """Check if can allocate.

        Args:
            line (OrderLine): order line value object.

        Returns:
            bool: True if can allocate.

        """
        return (
            self.stock_keeping_unit == line.stock_keeping_unit
            and self.available_quantity >= line.quantity
        )

    @property
    def allocated_quantity(self) -> int:
        """Get allocated quantity.

        Returns:
            int: allocated quantity.

        """
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        """Get available quantity.

        Returns:
            int: available quantity.

        """
        return self._purchased_quantity - self.allocated_quantity

    def __gt__(self, other: Self) -> bool:
        """Check is self greater than other.

        Args:
            other (Self): other batch entity.

        Returns:
            bool: True if greater.

        """
        if self.estimated_arrival_time is None:
            return False

        if other.estimated_arrival_time is None:
            return True

        return self.estimated_arrival_time > other.estimated_arrival_time
