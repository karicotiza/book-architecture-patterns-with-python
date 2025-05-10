"""SQL repository mock."""

from src.domain.aggregates.product import Product


class SQLRepositoryMock:
    """SQL repository mock."""

    def __init__(self, products: list[Product]) -> None:
        """Create new instance.

        Args:
            products (list[Batch]): initial data.

        """
        self._products = set(products)

    def get(self, stock_keeping_unit: str) -> Product | None:
        """Get product aggregate from repository by reference.

        Args:
            stock_keeping_unit (str): stock keeping unit.

        Returns:
            Product: product aggregate

        """
        product: Product | None = None

        try:
            product = next(
                product
                for product in self._products
                if product.stock_keeping_unit == stock_keeping_unit
            )
        except StopIteration:
            product = None

        return product

    def add(self, product: Product) -> None:
        """Add product aggregate to repository.

        Args:
            product (Product): product aggregate.

        """
        self._products.add(product)
