"""Pytest configuration."""

import pytest

from src.domain.repositories.file_system import IFileSystem
from src.domain.services.sync import SyncService
from src.infrastructure.repositories.fake_file_system import FakeFileSystem


@pytest.fixture
def sync_service() -> SyncService:
    """Sync service fixture.

    Returns:
        SyncService: sync service.

    """
    return SyncService()


@pytest.fixture
def file_system() -> IFileSystem:
    """File system fixture.

    Returns:
        IFileSystem: file system.

    """
    return FakeFileSystem()
