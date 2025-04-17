"""Tests for SQL alchemy repository."""

from collections.abc import Generator
from typing import Any

import pytest
from sqlalchemy import Engine, Result, create_engine, text
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from src.domain.entities.batch import Batch
from src.infrastructure.repositories.sql_repository.postgresql import (
    PostgreSQLRepository,
    create_mappers,
    metadata,
)


@pytest.fixture
def session() -> Generator[Session, None, None]:
    """Session fixture.

    Yields:
        Generator[Session, None, None]: Session.

    """
    engine: Engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)

    create_mappers()
    yield sessionmaker(engine)()
    clear_mappers()


def _insert_order_line(session: Session) -> str:
    session.execute(
        statement=text(
            "INSERT INTO order_lines (order_id, stock_keeping_unit, quantity) "
            'VALUES ("order-001", "GENERIC-SOFA", 12)'
        ),
    )

    order_line_id: Result[Any] = session.execute(
        statement=text(
            "SELECT id "
            "FROM order_lines "
            "WHERE order_id=:order_id "
            "AND stock_keeping_unit=:stock_keeping_unit"
        ),
        params={
            "order_id": "order-001",
            "stock_keeping_unit": "GENERIC-SOFA",
        },
    )

    return str(order_line_id)


def _insert_batch(session: Session, batch_id: str) -> str:
    session.execute(
        statement=text(
            "INSERT INTO batches (reference, stock_keeping_unit, "
            "_purchased_quantity, estimated_arrival_time) "
            'VALUES (:batch_id, "GENERIC-SOFA", 100, null)'
        ),
        params={
            "batch_id": batch_id,
        },
    )

    new_batch_id: Result[Any] = session.execute(
        statement=text(
            "SELECT id "
            "FROM batches "
            'WHERE reference=:batch_id AND stock_keeping_unit="GENERIC-SOFA"'
        ),
        params={
            "batch_id": batch_id,
        },
    )

    return str(new_batch_id)


def _insert_allocation(
    session: Session,
    order_line_id: str,
    batch_id: str,
) -> None:
    session.execute(
        statement=text(
            "INSERT INTO allocations (order_line_id, batch_id) "
            "VALUES (:order_line_id, :batch_id)"
        ),
        params={
            "order_line_id": order_line_id,
            "batch_id": batch_id,
        },
    )


def test_repository_can_save_batch(session: Session) -> None:
    """Test sql alchemy repository can save batch.

    Args:
        session (Session): sql alchemy orm session.

    """
    batch: Batch = Batch(
        reference="batch-001",
        stock_keeping_unit="RUSTY-SOAPDISH",
        quantity=100,
        estimated_arrival_time=None,
    )

    repository: PostgreSQLRepository = PostgreSQLRepository(session)
    repository.add(batch)
    session.commit()

    rows: list = list(
        session.execute(
            statement=text(
                "SELECT reference, stock_keeping_unit, _purchased_quantity, "
                "estimated_arrival_time "
                'FROM "batches"'
            )
        ).all()
    )

    assert rows == [("batch-001", "RUSTY-SOAPDISH", 100, None)]


def test_repository_can_get_batch(session: Session) -> None:
    """Test sql alchemy repository can get batch.

    Args:
        session (Session): sql alchemy orm session.

    """
    order_line_id = _insert_order_line(session)
    batch1_id = _insert_batch(session, "batch-002")
    _insert_batch(session, "batch-003")
    _insert_allocation(session, order_line_id, batch1_id)

    repo: PostgreSQLRepository = PostgreSQLRepository(session)
    retrieved: Batch = repo.get("batch-002")

    excepted = Batch(
        reference="batch-002",
        stock_keeping_unit="GENERIC-SOFA",
        quantity=100,
        estimated_arrival_time=None,
    )

    assert retrieved.stock_keeping_unit == excepted.stock_keeping_unit
