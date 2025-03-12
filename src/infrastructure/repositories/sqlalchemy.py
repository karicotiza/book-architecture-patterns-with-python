"""SQL alchemy repository."""

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

from src.domain.entities.batch import Batch
from src.domain.repositories.repository import IRepository
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

batches: Table = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(STRING_MAX_LENGTH)),
    Column("stock_keeping_unit", String(STRING_MAX_LENGTH)),
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
    lines_mapper: Mapper = registry().map_imperatively(OrderLine, order_lines)
    registry().map_imperatively(
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


class SQLAlchemyRepository(IRepository):
    """SQL alchemy repository."""

    def __init__(self, session: Session) -> None:
        """Create new instance.

        Args:
            session (Session): sql alchemy orm session.

        """
        self._session: Session = session

    def add(self, batch: Batch) -> None:
        """Add batch entity to repository.

        Args:
            batch (Batch): batch entity.

        """
        self._session.add(batch)

    def get(self, reference: str) -> Batch:
        """Get batch entity from repository by reference.

        Args:
            reference (str): batch entity reference.

        Returns:
            Batch: batch entity

        """
        return self._session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> list[Batch]:
        """Get all batch entities from repository.

        Returns:
            list[Batch]: list of batch entities.

        """
        return self._session.query(Batch).all()
