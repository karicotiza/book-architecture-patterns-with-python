"""Allocation application service tests."""

import pytest
from sqlalchemy.orm import Session

from src.application.services.allocation import (
    AllocationAppService,
    InvalidSKUError,
)
from src.domain.entities.batch import Batch
from src.domain.value_objects.order_line import OrderLine
from tests.mocks.infrastructure.repositories.sql_repository import (
    SQLRepositoryMock,
)


@pytest.fixture
def allocation_app_service() -> AllocationAppService:
    """Allocation app service fixture.

    Returns:
        AllocationAppService: allocation app service.

    """
    return AllocationAppService()


@pytest.mark.parametrize(
    argnames="batch_reference",
    argvalues=[
        ("BATCH-REFERENCE-001"),
    ],
)
def test_return_allocation(
    batch_reference: str,
    allocation_app_service: AllocationAppService,
    session: Session,
) -> None:
    """Test return allocation."""
    order_line: OrderLine = OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch: Batch = Batch(
        reference=batch_reference,
        stock_keeping_unit="COMPLICATED-LAMP",
        quantity=100,
        estimated_arrival_time=None,
    )

    sql_repository: SQLRepositoryMock = SQLRepositoryMock(
        batches=[batch],
    )

    reference = allocation_app_service.allocate(
        order_line=order_line,
        repository=sql_repository,
        session=session,
    )

    assert reference == batch_reference


def test_error_for_invalid_sku(
    allocation_app_service: AllocationAppService,
    session: Session,
) -> None:
    """Test error for invalid sku."""
    order_line: OrderLine = OrderLine("o1", "NONEXISTENDSKU", 10)
    batch = Batch(
        reference="b1",
        stock_keeping_unit="AREALSKU",
        quantity=100,
        estimated_arrival_time=None,
    )

    sql_repository: SQLRepositoryMock = SQLRepositoryMock(
        batches=[batch],
    )

    msg: str = f"Invalid SKU: {order_line.stock_keeping_unit}"
    with pytest.raises(InvalidSKUError, match=msg):
        allocation_app_service.allocate(
            order_line=order_line,
            repository=sql_repository,
            session=session,
        )
