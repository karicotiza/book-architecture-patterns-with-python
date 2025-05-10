"""Product aggregate."""

from src.domain.entities.batch import Batch
from src.domain.exceptions.out_of_stock import OutOfStockError
from src.domain.value_objects.order_line import OrderLine


class Product:
    """Product aggregate."""

    def __init__(
        self,
        stock_keeping_unit: str,
        batches: list[Batch],
        version_number: int = 0,
    ) -> None:
        """Create new instance.

        Args:
            stock_keeping_unit (str): stock keeping unit.
            batches (list[Batch]): batches.
            version_number (int, optional): version number. Defaults to 0.

        """
        self.stock_keeping_unit = stock_keeping_unit
        self.batches: list[Batch] = batches
        self.version_number: int = version_number

    def allocate(
        self,
        line: OrderLine,
    ) -> str:
        """Allocate order line.

        Args:
            line (OrderLine): order line

        Raises:
            OutOfStockError: if out of stock.

        Returns:
            str: batch reference.

        """
        try:
            batch = next(
                batch
                for batch in sorted(self.batches)
                if batch.can_allocate(line)
            )

        except StopIteration:
            msg: str = f"Article {line.stock_keeping_unit} is out of stock"
            raise OutOfStockError(msg) from StopIteration

        batch.allocate(line)
        self.version_number += 1

        return batch.reference
