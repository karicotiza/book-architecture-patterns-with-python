"""SQL repository interface."""

from typing import Protocol

from src.domain.aggregates.product import Product


class SQLRepository(Protocol):
    """SQL repository interface."""

    def get(self, stock_keeping_unit: str) -> Product | None:
        """Get product aggregate from repository by stock keeping unit.

        Args:
            stock_keeping_unit (str): stock keeping unit.

        Returns:
            Product | None: product aggregate.

        """
        ...

    def add(self, product: Product) -> None:
        """Add product aggregate to repository.

        Args:
            product (Product): product aggregate.

        """
        ...
