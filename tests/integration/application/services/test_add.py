"""Add application service tests."""

import pytest

from src.application.services.add import AddAppService
from tests.mocks.infrastructure.uow.allocation import AllocationUOWMock


@pytest.fixture
def add_app_service() -> AddAppService:
    """Add app service fixture.

    Returns:
        AddAppService: add app service.

    """
    return AddAppService()


def test_add_batch(add_app_service: AddAppService) -> None:
    """Test add app service's add_batch method.

    Args:
        add_app_service (AddAppService): add app service.
        session (Session): session.

    """
    unit_of_work: AllocationUOWMock = AllocationUOWMock()

    add_app_service.add_batch(
        batch=("b1", "CRUNCHY-ARMCHAIR", 100, None),
        unit_of_work=unit_of_work,
    )

    assert unit_of_work.batches.get("b1") is not None
