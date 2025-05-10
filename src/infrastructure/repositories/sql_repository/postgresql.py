"""PostgreSQL repository."""

from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import Session, registry, relationship

from src.domain.aggregates.product import Product
from src.domain.entities.batch import Batch
from src.domain.value_objects.order_line import OrderLine

if TYPE_CHECKING:
    from sqlalchemy.orm.mapper import Mapper


STRING_MAX_LENGTH = 255

metadata: MetaData = MetaData()

order_lines: Table = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("stock_keeping_unit", String(STRING_MAX_LENGTH)),
    Column("quantity", Integer, nullable=False),
    Column("order_id", String(STRING_MAX_LENGTH)),
)

products = Table(
    "products",
    metadata,
    Column("stock_keeping_unit", String(STRING_MAX_LENGTH), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
)

batches: Table = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(STRING_MAX_LENGTH)),
    Column("stock_keeping_unit", ForeignKey("products.stock_keeping_unit")),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("estimated_arrival_time", Date, nullable=True),
)

allocations: Table = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_line_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def create_mappers() -> None:
    """Do ORM mapping."""
    lines_mapper: Mapper = registry().map_imperatively(
        class_=OrderLine,
        local_table=order_lines,
    )

    batches_mapper: Mapper = registry().map_imperatively(
        class_=Batch,
        local_table=batches,
        properties={
            "_allocations": relationship(
                argument=lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )

    registry().map_imperatively(
        class_=Product,
        local_table=products,
        properties={"batches": relationship(batches_mapper)},
    )


class PostgreSQLRepository:
    """PostgreSQL repository."""

    def __init__(self, session: Session) -> None:
        """Create new instance.

        Args:
            session (Session): SQLAlchemy's session.

        """
        self._session: Session = session

    def get(self, stock_keeping_unit: str) -> Product | None:
        """Get product aggregate from repository by stock keeping unit.

        Args:
            stock_keeping_unit (str): stock keeping unit.

        Returns:
            Product: product aggregate.

        """
        return (
            self._session.query(Product)
            .filter_by(stock_keeping_unit=stock_keeping_unit)
            .first()
        )

    def add(self, product: Product) -> None:
        """Add product aggregate to repository.

        Args:
            product (Product): product aggregate.

        """
        self._session.add(product)

    def truncate(self) -> None:
        """Truncate tables."""
        for table in reversed(metadata.sorted_tables):
            self._session.execute(table.delete())

        self._session.commit()
