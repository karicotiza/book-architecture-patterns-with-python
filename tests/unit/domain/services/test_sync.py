"""Test sync domain service."""

from pathlib import Path

import pytest

from src.domain.interfaces.repositories.file_system import IFileSystem
from src.domain.services.reader import Reader
from src.domain.services.sync import SyncService
from src.domain.value_objects.file_system_command import FileSystemCommand
from src.domain.value_objects.file_system_command_action import (
    FileSystemCommandAction,
)


@pytest.mark.parametrize(
    argnames=(
        "source",
        "destination",
    ),
    argvalues=[
        (
            {"sha1": "my-file"},
            {},
        ),
    ],
)
def test_sync_service_sync_when_exists(
    source: dict[str, str],
    destination: dict[str, str],
    sync_service: SyncService,
    file_system: IFileSystem,
) -> None:
    """Test sync service's sync method.

    Test when a file exists in source but not in destination.

    Args:
        source (dict[str, str]): source content.
        destination (dict[str, str]): destination content.
        sync_service (SyncService): sync service.
        file_system (IFileSystem): file system repository.

    """
    reader: Reader = Reader(
        source=source,
        destination=destination,
    )

    sync_service.sync(
        reader=reader,
        file_system=file_system,
        source="/source",
        destination="/destination",
    )

    assert file_system.history() == [
        FileSystemCommand(
            command=FileSystemCommandAction.copy,
            source=Path("/source/my-file"),
            destination=Path("/destination/my-file"),
        )
    ]


@pytest.mark.parametrize(
    argnames=(
        "source",
        "destination",
    ),
    argvalues=[
        (
            {"sha1": "renamed-file"},
            {"sha1": "original-file"},
        ),
    ],
)
def test_sync_service_sync_when_renamed(
    source: dict[str, str],
    destination: dict[str, str],
    sync_service: SyncService,
    file_system: IFileSystem,
) -> None:
    """Test sync service's sync method.

    Test when a file has been renamed in the source.

    Args:
        source (dict[str, str]): source content.
        destination (dict[str, str]): destination content.
        sync_service (SyncService): sync service.
        file_system (IFileSystem): file system repository.

    """
    reader: Reader = Reader(
        source=source,
        destination=destination,
    )

    sync_service.sync(
        reader=reader,
        file_system=file_system,
        source="/source",
        destination="/destination",
    )

    assert file_system.history() == [
        FileSystemCommand(
            command=FileSystemCommandAction.move,
            source=Path("/destination/original-file"),
            destination=Path("/destination/renamed-file"),
        )
    ]
