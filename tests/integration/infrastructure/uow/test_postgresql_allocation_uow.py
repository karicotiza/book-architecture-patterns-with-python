"""Test PostgreSQL allocation unit of work."""

from collections.abc import Callable
from datetime import date
from typing import Any

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.aggregates.product import Product
from src.domain.entities.batch import Batch
from src.domain.value_objects.order_line import OrderLine
from src.infrastructure.uow.allocation.postgresql_allocation import (
    PostgresqlAllocationUOW,
)
from tests.mocks.infrastructure.uow.allocation import AllocationUOWMock

BATCH_REFERENCE: str = "batch_reference"
STOCK_KEEPING_UNIT: str = "stock_keeping_unit"
QUANTITY: str = "quantity"
ESTIMATED_ARRIVAL_TIME: str = "estimated_arrival_time"


def insert_batch(
    session: Session,
    batch: tuple[str, str, str, date | None, int],
) -> None:
    """Insert batch.

    Args:
        session (Session): SQLAlchemy's session.
        batch (tuple[str, str, str, date | None, int]): batch reference,
            stock keeping unit, quantity, estimated arrival time and
            version number.

    """
    session.execute(
        statement=text(
            "INSERT INTO products (stock_keeping_unit, version_number) "
            "VALUES (:stock_keeping_unit, :version_number)"
        ),
        params={
            "stock_keeping_unit": batch[1],
            "version_number": batch[4],
        },
    )

    session.execute(
        statement=text(
            "INSERT INTO batches (reference, stock_keeping_unit,"
            " _purchased_quantity, estimated_arrival_time) "
            "VALUES (:reference, :stock_keeping_unit, :_purchased_quantity,"
            " :estimated_arrival_time)"
        ),
        params={
            "reference": batch[0],
            "stock_keeping_unit": batch[1],
            "_purchased_quantity": batch[2],
            "estimated_arrival_time": batch[3],
        },
    )


def get_allocated_batch_ref(
    session: Session,
    order_id: str,
    stock_keeping_unit: str,
) -> str:
    """Get allocated batch reference.

    Args:
        session (Session): SQLAlchemy's session.
        order_id (str): order id.
        stock_keeping_unit (str): stock keeping unit.

    Returns:
        str: batch reference.

    """
    order_line_id: Any = session.execute(
        statement=text(
            "SELECT id "
            "FROM order_lines "
            "WHERE order_id=:order_id"
            " AND stock_keeping_unit=:stock_keeping_unit"
        ),
        params={
            "order_id": order_id,
            STOCK_KEEPING_UNIT: stock_keeping_unit,
        },
    ).scalar_one()

    batch_reference: Any = session.execute(
        statement=text(
            "SELECT batch.reference "
            "FROM allocations "
            "JOIN batches AS batch ON batch_id = batch.id "
            "WHERE order_line_id=:order_line_id"
        ),
        params={
            "order_line_id": order_line_id,
        },
    ).scalar_one()

    return batch_reference


@pytest.mark.parametrize(
    argnames=(
        BATCH_REFERENCE,
        STOCK_KEEPING_UNIT,
        QUANTITY,
        ESTIMATED_ARRIVAL_TIME,
    ),
    argvalues=[("batch-001", "HIPSTER-WORKBENCH", 100, None)],
)
def test_can_retrieve_a_batch_and_allocate_to_it(
    batch_reference: str,
    stock_keeping_unit: str,
    quantity: int,
    estimated_arrival_time: date | None,
    session_factory: Callable[[], Session],
) -> None:
    """Test UOW can retrieve a batch and allocate to it.

    Args:
        batch_reference (str): batch reference.
        stock_keeping_unit (str): stock keeping unit.
        quantity (int): quantity.
        estimated_arrival_time (date | None): estimated arrival time.
        session_factory (Callable[[], Session]): session factory.

    """
    session: Session = session_factory()

    insert_batch(
        session=session,
        batch=(
            batch_reference,
            stock_keeping_unit,
            str(quantity),
            estimated_arrival_time,
            1,
        ),
    )

    unit_of_work: PostgresqlAllocationUOW = PostgresqlAllocationUOW(
        session_factory=session_factory,
    )

    with unit_of_work:
        product: Product | None = unit_of_work.products.get(stock_keeping_unit)

        order_line: OrderLine = OrderLine(
            order_id="order-line-001",
            stock_keeping_unit=stock_keeping_unit,
            quantity=10,
        )

        if isinstance(product, Product):
            product.allocate(order_line)
            unit_of_work.commit()

    allocated_batch_reference: str = get_allocated_batch_ref(
        session=session,
        order_id="order-line-001",
        stock_keeping_unit=stock_keeping_unit,
    )

    assert allocated_batch_reference == batch_reference


@pytest.mark.parametrize(
    argnames=(
        BATCH_REFERENCE,
        STOCK_KEEPING_UNIT,
        QUANTITY,
        ESTIMATED_ARRIVAL_TIME,
    ),
    argvalues=[("batch-002", "COMPLICATED-LAMP", 100, None)],
)
def test_add_batch(
    batch_reference: str,
    stock_keeping_unit: str,
    quantity: int,
    estimated_arrival_time: date | None,
) -> None:
    """Test add batch.

    Args:
        batch_reference (str): batch reference.
        stock_keeping_unit (str): stock keeping unit.
        quantity (int): quantity.
        estimated_arrival_time (date | None): estimated arrival time.

    """
    uow: AllocationUOWMock = AllocationUOWMock()
    uow.products.add(
        product=Product(
            stock_keeping_unit=stock_keeping_unit,
            batches=[
                Batch(
                    reference=batch_reference,
                    stock_keeping_unit=stock_keeping_unit,
                    quantity=quantity,
                    estimated_arrival_time=estimated_arrival_time,
                ),
            ],
            version_number=0,
        )
    )

    uow.commit()

    assert uow.products.get(stock_keeping_unit) is not None
    assert uow.committed


@pytest.mark.parametrize(
    argnames=(
        BATCH_REFERENCE,
        STOCK_KEEPING_UNIT,
        QUANTITY,
        ESTIMATED_ARRIVAL_TIME,
    ),
    argvalues=[("batch-003", "COMPLICATED-LAMP", 100, None)],
)
def test_allocate_returns_allocation(
    batch_reference: str,
    stock_keeping_unit: str,
    quantity: int,
    estimated_arrival_time: date | None,
) -> None:
    """Test allocate returns allocation.

    Args:
        batch_reference (str): batch reference.
        stock_keeping_unit (str): stock keeping unit.
        quantity (int): quantity.
        estimated_arrival_time (date | None): estimated arrival time.

    """
    uow: AllocationUOWMock = AllocationUOWMock()

    uow.products.add(
        product=Product(
            stock_keeping_unit=stock_keeping_unit,
            batches=[
                Batch(
                    reference=batch_reference,
                    stock_keeping_unit=stock_keeping_unit,
                    quantity=quantity,
                    estimated_arrival_time=estimated_arrival_time,
                )
            ],
            version_number=0,
        ),
    )

    product: Product | None = uow.products.get(stock_keeping_unit)

    if isinstance(product, Product):
        allocated_batch: str = product.allocate(
            line=OrderLine(
                order_id="order-003",
                stock_keeping_unit=stock_keeping_unit,
                quantity=quantity,
            )
        )

        assert allocated_batch == batch_reference


@pytest.mark.parametrize(
    argnames=(
        BATCH_REFERENCE,
        STOCK_KEEPING_UNIT,
        QUANTITY,
        ESTIMATED_ARRIVAL_TIME,
    ),
    argvalues=[("batch-004", "MEDIUM-PLINTH", 100, None)],
)
def test_rolls_back_uncommitted_work_by_default(
    batch_reference: str,
    stock_keeping_unit: str,
    quantity: int,
    estimated_arrival_time: date | None,
    session_factory: Callable[[], Session],
) -> None:
    """Test rolls back uncommitted by default.

    Args:
        batch_reference (str): batch reference.
        stock_keeping_unit (str): stock keeping unit.
        quantity (int): quantity.
        estimated_arrival_time (date | None): estimated arrival time.
        session_factory (Callable[[], Session]): session factory.

    """
    uow: PostgresqlAllocationUOW = PostgresqlAllocationUOW(session_factory)

    with uow:
        insert_batch(
            session=uow.session,
            batch=(
                batch_reference,
                stock_keeping_unit,
                str(quantity),
                estimated_arrival_time,
                1,
            ),
        )

    new_session: Session = session_factory()
    rows: list = list(
        new_session.execute(statement=text("SELECT * FROM 'batches'"))
    )

    assert rows == []


@pytest.mark.parametrize(
    argnames=(
        BATCH_REFERENCE,
        STOCK_KEEPING_UNIT,
        QUANTITY,
        ESTIMATED_ARRIVAL_TIME,
    ),
    argvalues=[("batch-002", "LARGE-FORK", 100, None)],
)
def test_rolls_back_on_error(
    batch_reference: str,
    stock_keeping_unit: str,
    quantity: int,
    estimated_arrival_time: date | None,
    session_factory: Callable[[], Session],
) -> None:
    """Test rolls back on error.

    Args:
        batch_reference (str): batch reference.
        stock_keeping_unit (str): stock keeping unit.
        quantity (int): quantity.
        estimated_arrival_time (date | None): estimated arrival time.
        session_factory (Callable[[], Session]): session factory.

    """
    uow: PostgresqlAllocationUOW = PostgresqlAllocationUOW(session_factory)
    msg: str = "Test error"

    with uow, pytest.raises(ValueError, match=msg):  # noqa: PT012
        insert_batch(
            session=uow.session,
            batch=(
                batch_reference,
                stock_keeping_unit,
                str(quantity),
                estimated_arrival_time,
                1,
            ),
        )
        raise ValueError(msg)

    new_session = session_factory()

    rows: list = list(
        new_session.execute(statement=text("SELECT * FROM 'batches'"))
    )

    assert rows == []
