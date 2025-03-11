"""Test batch entity."""

from datetime import UTC, datetime

import pytest

from src.domain.entities.batch import Batch
from src.domain.value_objects.order_line import OrderLine


@pytest.mark.parametrize(
    argnames=(
        "batch_quantity",
        "order_line_quantity",
        "repeat",
        "batch_available_quantity",
    ),
    argvalues=[
        (20, 2, 1, 18),
        (1, 2, 1, 1),
        (10, 2, 2, 6),
    ],
)
def test_batch_allocate_reduce_available_quantity(
    batch_quantity: int,
    order_line_quantity: int,
    repeat: int,
    batch_available_quantity: int,
) -> None:
    """Test allocating to a batch reduces the available quantity.

    Args:
        batch_quantity (int): batch quantity.
        order_line_quantity (int): order line quantity.
        repeat (int): number of same allocations.
        batch_available_quantity (int): batch available quantity.

    """
    batch: Batch = Batch(
        ref="batch-001",
        sku="SMALL-TABLE",
        qty=batch_quantity,
        eta=datetime.now(UTC).date(),
    )

    for index in range(repeat):
        line: OrderLine = OrderLine(
            order_id=f"order-ref-00{index}",
            sku="SMALL-TABLE",
            qty=order_line_quantity,
        )

        batch.allocate(line)

    assert batch.available_quantity == batch_available_quantity


@pytest.mark.parametrize(
    argnames=(
        "batch_sku",
        "order_line_sku",
        "batch_quantity",
        "order_line_quantity",
        "can_allocate",
    ),
    argvalues=[
        ("ELEGANT_LAMP", "ELEGANT_LAMP", 20, 2, True),
        ("LONG_LAMP", "LONG_LAMP", 2, 20, False),
        ("BRIGHT_LAMP", "BRIGHT_LAMP", 2, 2, True),
        ("UNCOMFORTABLE-CHAIR", "EXPENSIVE-TOASTER", 100, 10, False),
    ],
)
def test_batch_can_allocate(
    batch_sku: str,
    order_line_sku: str,
    batch_quantity: int,
    order_line_quantity: int,
    *,
    can_allocate: bool,
) -> None:
    """Test batch can_allocate method.

    Args:
        batch_sku (str): batch stock keeping unit.
        order_line_sku (str): order line stock keeping unit.
        batch_quantity (int): batch quantity.
        order_line_quantity (int): order line quantity.
        can_allocate (bool): expected result.

    """
    batch: Batch = Batch(
        ref="batch-001",
        sku=batch_sku,
        qty=batch_quantity,
        eta=datetime.now(UTC).date(),
    )

    line: OrderLine = OrderLine(
        order_id="order-ref-001",
        sku=order_line_sku,
        qty=order_line_quantity,
    )

    assert batch.can_allocate(line) is can_allocate


@pytest.mark.parametrize(
    argnames=(
        "batch_sku",
        "order_line_sku",
        "batch_quantity",
        "order_line_quantity",
        "batch_available_quantity",
    ),
    argvalues=[
        ("DECORATIVE-TRINKET", "DECORATIVE-TRINKET", 20, 2, 20),
    ],
)
def test_batch_deallocate(
    batch_sku: str,
    order_line_sku: str,
    batch_quantity: int,
    order_line_quantity: int,
    batch_available_quantity: int,
) -> None:
    """Test batch deallocate method.

    Args:
        batch_sku (str): _description_
        order_line_sku (str): _description_
        batch_quantity (int): _description_
        order_line_quantity (int): _description_
        batch_available_quantity (int): _description_

    """
    batch: Batch = Batch(
        ref="batch-001",
        sku=batch_sku,
        qty=batch_quantity,
        eta=datetime.now(UTC).date(),
    )

    line: OrderLine = OrderLine(
        order_id="order-ref-001",
        sku=order_line_sku,
        qty=order_line_quantity,
    )

    batch.deallocate(line)

    assert batch.available_quantity == batch_available_quantity
