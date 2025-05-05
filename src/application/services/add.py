"""Add application service."""

from datetime import date

from src.domain.entities.batch import Batch
from src.domain.interfaces.uow.allocation import AllocationUOW


class AddAppService:
    """Add application service."""

    def add_batch(
        self,
        batch: tuple[str, str, int, date | None],
        unit_of_work: AllocationUOW,
    ) -> None:
        """Add batch to repository.

        Args:
            batch (str): reference, stock keeping unit, quantity and
                estimated arrival time.
            repository (SQLRepository): sql repository.
            unit_of_work (AllocationUOW): AllocationUOW.

        """
        with unit_of_work:
            unit_of_work.batches.add(
                batch=Batch(
                    reference=batch[0],
                    stock_keeping_unit=batch[1],
                    quantity=batch[2],
                    estimated_arrival_time=batch[3],
                )
            )

            unit_of_work.commit()
