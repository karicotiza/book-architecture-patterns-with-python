"""BatchEntity."""

from datetime import date
from typing import Self

from src.domain.value_objects.order_line import OrderLine


class Batch:
    """Batch entity."""

    def __init__(
        self,
        ref: str,
        sku: str,
        qty: int,
        eta: date | None,
    ) -> None:
        """Create new instance.

        Args:
            ref (str): order reference.
            sku (str): stock keeping unit.
            qty (int): quantity.
            eta (date | None): estimated arrival time.

        """
        self.reference: str = ref
        self.sku: str = sku
        self.eta: date | None = eta
        self._purchased_quantity: int = qty
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
        return self.sku == line.sku and self.available_quantity >= line.qty

    @property
    def allocated_quantity(self) -> int:
        """Get allocated quantity.

        Returns:
            int: allocated quantity.

        """
        return sum(line.qty for line in self._allocations)

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
        if self.eta is None:
            return False

        if other.eta is None:
            return True

        return self.eta > other.eta
