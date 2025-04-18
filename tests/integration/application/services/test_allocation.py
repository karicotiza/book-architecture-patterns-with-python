"""Allocation application service tests."""

from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

from src.application.services.add import AddAppService
from src.application.services.allocation import (
    AllocationAppService,
    InvalidSKUError,
)
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


@pytest.fixture
def add_app_service() -> AddAppService:
    """Add app service fixture.

    Returns:
        AddAppService: add app service.

    """
    return AddAppService()


@pytest.mark.parametrize(
    argnames="batch_reference",
    argvalues=[
        ("BATCH-REFERENCE-001"),
    ],
)
def test_return_allocation(
    batch_reference: str,
    allocation_app_service: AllocationAppService,
    add_app_service: AddAppService,
    session: Session,
) -> None:
    """Test return allocation."""
    sql_repository: SQLRepositoryMock = SQLRepositoryMock([])

    add_app_service.add_batch(
        batch=(batch_reference, "COMPLICATED-LAMP", 100, None),
        repository=sql_repository,
        session=session,
    )

    reference = allocation_app_service.allocate(
        order_id="o1",
        stock_keeping_unit="COMPLICATED-LAMP",
        quantity=10,
        repository=sql_repository,
        session=session,
    )

    assert reference == batch_reference


def test_error_for_invalid_sku(
    allocation_app_service: AllocationAppService,
    add_app_service: AddAppService,
    session: Session,
) -> None:
    """Test error for invalid sku."""
    sql_repository: SQLRepositoryMock = SQLRepositoryMock([])

    add_app_service.add_batch(
        batch=("b1", "AREALSKU", 100, None),
        repository=sql_repository,
        session=session,
    )

    msg: str = "Invalid SKU: NONEXISTENDSKU"
    with pytest.raises(InvalidSKUError, match=msg):
        allocation_app_service.allocate(
            order_id="o1",
            stock_keeping_unit="NONEXISTENDSKU",
            quantity=10,
            repository=sql_repository,
            session=session,
        )


@pytest.mark.parametrize(
    argnames=(
        "initial_batch_quantity",
        "order_line_quantity",
    ),
    argvalues=[
        (100, 10),
    ],
)
def test_prefers_warehouse(
    initial_batch_quantity: int,
    order_line_quantity: int,
    allocation_app_service: AllocationAppService,
    add_app_service: AddAppService,
    session: Session,
) -> None:
    """Test prefers warehouse batches to shipment batches.

    Args:
        initial_batch_quantity (int): initial batch quantity.
        order_line_quantity (int): order line quantity.
        allocation_app_service (AllocationAppService): allocation app service.
        add_app_service (AddAppService): add app service.
        session (Session): session.

    """
    sql_repository: SQLRepositoryMock = SQLRepositoryMock([])

    add_app_service.add_batch(
        batch=("batch-001", "RETRO-CLOCK", initial_batch_quantity, None),
        repository=sql_repository,
        session=session,
    )

    add_app_service.add_batch(
        batch=(
            "batch-002",
            "RETRO-CLOCK",
            initial_batch_quantity,
            datetime.now(UTC),
        ),
        repository=sql_repository,
        session=session,
    )

    allocation_app_service.allocate(
        order_id="order-line-001",
        stock_keeping_unit="RETRO-CLOCK",
        quantity=order_line_quantity,
        repository=sql_repository,
        session=session,
    )

    assert (
        sql_repository.get("batch-001").available_quantity
        == initial_batch_quantity - order_line_quantity
    )

    assert (
        sql_repository.get("batch-002").available_quantity
        == initial_batch_quantity
    )
