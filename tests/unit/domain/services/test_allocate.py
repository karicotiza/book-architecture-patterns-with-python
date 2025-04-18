"""Tests for allocation domain service."""

from datetime import UTC, datetime, timedelta

import pytest

from src.domain.entities.batch import Batch
from src.domain.exceptions.out_of_stock import OutOfStockError
from src.domain.services.allocate import AllocationService
from src.domain.value_objects.order_line import OrderLine


@pytest.mark.parametrize(
    argnames=(
        "earliest",
        "medium",
        "latest",
    ),
    argvalues=[
        (
            datetime.now(UTC),
            datetime.now(UTC) + timedelta(days=1),
            datetime.now(UTC) + timedelta(weeks=4),
        ),
    ],
)
def test_allocate_prefers_earlier_batches(
    earliest: datetime,
    medium: datetime,
    latest: datetime,
) -> None:
    """Test allocation service allocate method prefer earlier batches.

    Args:
        earliest (datetime): estimated arrival time date of the earliest batch.
        medium (datetime): estimated arrival time date of the medium batch.
        latest (datetime): estimated arrival time date of the latest batch.

    """
    stock_keeping_unit: str = "MINIMALIST-SPOON"
    allocation_service: AllocationService = AllocationService()
    initial_available_quantity: int = 100
    expected_available_quantity: int = 90

    batches: list[Batch] = [
        Batch(
            reference="batch-002",
            stock_keeping_unit=stock_keeping_unit,
            quantity=initial_available_quantity,
            estimated_arrival_time=estimated_arrival_time,
        )
        for estimated_arrival_time in (earliest, medium, latest)
    ]

    allocation_service.allocate(
        order_line=OrderLine(
            order_id="order-line-002",
            stock_keeping_unit=stock_keeping_unit,
            quantity=10,
        ),
        batches=batches,
    )

    assert batches[0].available_quantity == expected_available_quantity
    assert batches[1].available_quantity == initial_available_quantity
    assert batches[2].available_quantity == initial_available_quantity


@pytest.mark.parametrize(
    argnames="reference",
    argvalues=[
        ("batch-003",),
    ],
)
def test_allocate_returns_allocated_batch_ref(
    reference: str,
) -> None:
    """Test allocation service allocate method returns batch reference.

    Args:
        reference (str): allocated batch reference.

    """
    allocation_service: AllocationService = AllocationService()

    is_stock_batch: Batch = Batch(
        reference=reference,
        stock_keeping_unit="HIGHBROW_POSTER",
        quantity=100,
        estimated_arrival_time=None,
    )

    shipment_batch: Batch = Batch(
        reference="batch-003",
        stock_keeping_unit="HIGHBROW_POSTER",
        quantity=100,
        estimated_arrival_time=None,
    )

    order_line: OrderLine = OrderLine(
        order_id="order-line-003",
        stock_keeping_unit="HIGHBROW_POSTER",
        quantity=10,
    )

    assert (
        allocation_service.allocate(
            order_line=order_line, batches=[is_stock_batch, shipment_batch]
        )
        == reference
    )


@pytest.mark.parametrize(
    argnames=(
        "batch_quantity",
        "order_line_quantity",
    ),
    argvalues=[
        (10, (10, 1)),
    ],
)
def test_allocate_raises_out_of_stock(
    batch_quantity: int,
    order_line_quantity: tuple[int, int],
) -> None:
    """Test allocation service allocate method raises out of stock error.

    Args:
        batch_quantity (int): batch quantity.
        order_line_quantity (tuple[int, int]): order line quantity for two
            allocations.

    """
    stock_keeping_unit: str = "SMALL-FORK"
    allocation_service: AllocationService = AllocationService()

    batch: Batch = Batch(
        reference="batch-004",
        stock_keeping_unit=stock_keeping_unit,
        quantity=batch_quantity,
        estimated_arrival_time=datetime.now(UTC).date(),
    )

    allocation_service.allocate(
        order_line=OrderLine(
            order_id="order-line-004",
            stock_keeping_unit=stock_keeping_unit,
            quantity=order_line_quantity[0],
        ),
        batches=[batch],
    )

    with pytest.raises(OutOfStockError, match=stock_keeping_unit):
        allocation_service.allocate(
            order_line=OrderLine(
                order_id="order-line-004",
                stock_keeping_unit=stock_keeping_unit,
                quantity=order_line_quantity[1],
            ),
            batches=[batch],
        )
