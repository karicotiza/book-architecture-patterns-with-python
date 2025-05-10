"""Allocation application service tests."""

from datetime import UTC, datetime

import pytest

from src.application.services.add import AddAppService
from src.application.services.allocation import (
    AllocationAppService,
    InvalidSKUError,
)
from src.domain.aggregates.product import Product
from src.infrastructure.uow.allocation.postgresql_allocation import (
    PostgresqlAllocationUOW,
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


@pytest.mark.usefixtures("sqlalchemy_mapping")
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
) -> None:
    """Test return allocation."""
    add_app_service.add_batch(
        batch=(batch_reference, "COMPLICATED-LAMP", 100, None),
        unit_of_work=PostgresqlAllocationUOW(),
    )

    reference = allocation_app_service.allocate(
        order_id="o1",
        stock_keeping_unit="COMPLICATED-LAMP",
        quantity=10,
        unit_of_work=PostgresqlAllocationUOW(),
    )

    assert reference == batch_reference


@pytest.mark.usefixtures("sqlalchemy_mapping")
def test_error_for_invalid_sku(
    allocation_app_service: AllocationAppService,
    add_app_service: AddAppService,
) -> None:
    """Test error for invalid sku."""
    add_app_service.add_batch(
        batch=("b1", "AREALSKU", 100, None),
        unit_of_work=PostgresqlAllocationUOW(),
    )

    msg: str = "Invalid SKU: NONEXISTENDSKU"
    with pytest.raises(InvalidSKUError, match=msg):
        allocation_app_service.allocate(
            order_id="o1",
            stock_keeping_unit="NONEXISTENDSKU",
            quantity=10,
            unit_of_work=PostgresqlAllocationUOW(),
        )


@pytest.mark.usefixtures("sqlalchemy_mapping")
@pytest.mark.parametrize(
    argnames=(
        "initial_batch_quantity",
        "order_line_quantity",
        "stock_keeping_unit",
    ),
    argvalues=[
        (100, 10, "RETRO-CLOCK"),
    ],
)
def test_prefers_warehouse(
    initial_batch_quantity: int,
    order_line_quantity: int,
    stock_keeping_unit: str,
    allocation_app_service: AllocationAppService,
    add_app_service: AddAppService,
) -> None:
    """Test prefers warehouse batches to shipment batches.

    Args:
        initial_batch_quantity (int): initial batch quantity.
        order_line_quantity (int): order line quantity.
        stock_keeping_unit (str): stock keeping unit.
        allocation_app_service (AllocationAppService): allocation app service.
        add_app_service (AddAppService): add app service.
        session (Session): session.

    """
    unit_of_work: PostgresqlAllocationUOW = PostgresqlAllocationUOW()

    with unit_of_work:
        unit_of_work.products.truncate()

    unit_of_work = PostgresqlAllocationUOW()

    add_app_service.add_batch(
        batch=("batch-001", stock_keeping_unit, initial_batch_quantity, None),
        unit_of_work=unit_of_work,
    )

    add_app_service.add_batch(
        batch=(
            "batch-002",
            stock_keeping_unit,
            initial_batch_quantity,
            datetime.now(UTC),
        ),
        unit_of_work=unit_of_work,
    )

    allocation_app_service.allocate(
        order_id="order-line-001",
        stock_keeping_unit=stock_keeping_unit,
        quantity=order_line_quantity,
        unit_of_work=unit_of_work,
    )

    product: Product | None = unit_of_work.products.get(stock_keeping_unit)

    if isinstance(product, Product):
        assert (
            product.batches[0].available_quantity
            == initial_batch_quantity - order_line_quantity
        )

        assert product.batches[1].available_quantity == initial_batch_quantity
