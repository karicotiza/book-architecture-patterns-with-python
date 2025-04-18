"""Add application service."""

from datetime import date

from sqlalchemy.orm import Session

from src.domain.entities.batch import Batch
from src.domain.interfaces.repositories.sql_repository import SQLRepository


class AddAppService:
    """Add application service."""

    def add_batch(
        self,
        batch: tuple[str, str, int, date | None],
        repository: SQLRepository,
        session: Session,
    ) -> None:
        """Add batch to repository.

        Args:
            batch (str): reference, stock keeping unit, quantity and
                estimated arrival time.
            repository (SQLRepository): sql repository.
            session (Session): session.

        """
        repository.add(
            batch=Batch(
                reference=batch[0],
                stock_keeping_unit=batch[1],
                quantity=batch[2],
                estimated_arrival_time=batch[3],
            )
        )

        session.commit()
