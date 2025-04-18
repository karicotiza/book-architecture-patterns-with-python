"""Add application service tests."""

import pytest
from sqlalchemy.orm import Session

from src.application.services.add import AddAppService
from tests.mocks.infrastructure.repositories.sql_repository import (
    SQLRepositoryMock,
)


@pytest.fixture
def add_app_service() -> AddAppService:
    """Add app service fixture.

    Returns:
        AddAppService: add app service.

    """
    return AddAppService()


def test_add_batch(
    add_app_service: AddAppService,
    session: Session,
) -> None:
    """Test add app service's add_batch method.

    Args:
        add_app_service (AddAppService): add app service.
        session (Session): session.

    """
    sql_repository: SQLRepositoryMock = SQLRepositoryMock([])

    add_app_service.add_batch(
        batch=("b1", "CRUNCHY-ARMCHAIR", 100, None),
        repository=sql_repository,
        session=session,
    )

    assert sql_repository.get("b1") is not None
