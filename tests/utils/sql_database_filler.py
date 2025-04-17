"""SQL database filler utility module."""

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.entities.batch import Batch


class SQLRepositoryFiller:
    """SQL repository filler."""

    def __init__(self, session: Session) -> None:
        """Create new instance."""
        self._session: Session = session

        self._added_batches_ids: set[str] = set()
        self._added_stock_keeping_units: set[str] = set()

    def add_batches(self, batches: list[Batch]) -> None:
        """Add batches.

        Args:
            batches (list[Batch]): list of batches.

        """
        for batch in batches:
            self._session.execute(
                statement=text(
                    "INSERT INTO batches (reference, stock_keeping_unit,"
                    " _purchased_quantity, estimated_arrival_time) "
                    "VALUES (:ref, :stock_keeping_unit, :qty,"
                    " :estimated_arrival_time)"
                ),
                params={
                    "ref": batch.reference,
                    "stock_keeping_unit": batch.stock_keeping_unit,
                    "qty": batch.available_quantity,
                    "estimated_arrival_time": batch.estimated_arrival_time,
                },
            )

            batch_id: str = (
                str(
                    self._session.execute(
                        statement=text(
                            "SELECT id "
                            "FROM batches "
                            "WHERE reference=:ref"
                            " AND stock_keeping_unit=:stock_keeping_unit",
                        ),
                        params={
                            "ref": batch.reference,
                            "stock_keeping_unit": batch.stock_keeping_unit,
                        },
                    ).scalar()
                )
                or ""
            )

            self._added_batches_ids.add(batch_id)
            self._added_stock_keeping_units.add(batch.stock_keeping_unit)

        self._session.commit()

    def delete_batches(self) -> None:
        """Delete batches."""
        for batch_id in self._added_batches_ids:
            self._session.execute(
                statement=text(
                    "DELETE FROM allocations WHERE batch_id=:batch_id"
                ),
                params={
                    "batch_id": batch_id,
                },
            )

            self._session.execute(
                statement=text("DELETE FROM batches WHERE id=:batch_id"),
                params={"batch_id": batch_id},
            )

        for stock_keeping_unit in self._added_stock_keeping_units:
            self._session.execute(
                statement=text(
                    "DELETE FROM order_lines "
                    "WHERE stock_keeping_unit=:stock_keeping_unit"
                ),
                params={
                    "stock_keeping_unit": stock_keeping_unit,
                },
            )

            self._session.commit()
