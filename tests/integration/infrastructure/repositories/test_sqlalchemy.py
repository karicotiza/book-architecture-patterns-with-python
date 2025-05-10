"""Tests for SQL alchemy repository."""

from collections.abc import Generator

import pytest
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from src.domain.aggregates.product import Product
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


def test_repository_can_save_batch(session: Session) -> None:
    """Test sql alchemy repository can save batch.

    Args:
        session (Session): sql alchemy orm session.

    """
    repository: PostgreSQLRepository = PostgreSQLRepository(session)
    repository.add(
        product=Product(
            stock_keeping_unit="RUSTY-SOAPDISH",
            batches=[
                Batch(
                    reference="batch-001",
                    stock_keeping_unit="RUSTY-SOAPDISH",
                    quantity=100,
                    estimated_arrival_time=None,
                ),
            ],
            version_number=0,
        ),
    )

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


@pytest.mark.parametrize(
    argnames="stock_keeping_unit",
    argvalues=[
        ("GENERIC-SOFA"),
    ],
)
def test_repository_can_get_batch(
    stock_keeping_unit: str, session: Session
) -> None:
    """Test sql alchemy repository can get batch.

    Args:
        stock_keeping_unit (str): stock keeping unit.
        session (Session): sql alchemy orm session.

    """
    repo: PostgreSQLRepository = PostgreSQLRepository(session)

    repo.add(
        product=Product(
            stock_keeping_unit=stock_keeping_unit,
            batches=[
                Batch(
                    reference="batch-002",
                    stock_keeping_unit=stock_keeping_unit,
                    quantity=100,
                    estimated_arrival_time=None,
                ),
                Batch(
                    reference="batch-003",
                    stock_keeping_unit=stock_keeping_unit,
                    quantity=100,
                    estimated_arrival_time=None,
                ),
            ],
            version_number=0,
        )
    )
    retrieved: Product | None = repo.get(stock_keeping_unit)

    if isinstance(retrieved, Product):
        assert retrieved.stock_keeping_unit == stock_keeping_unit
