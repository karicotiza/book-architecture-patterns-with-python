"""Fake file system repository."""

from pathlib import Path

from src.domain.repositories.file_system import IFileSystem
from src.domain.value_objects.file_system_command import FileSystemCommand
from src.domain.value_objects.file_system_command_action import (
    FileSystemCommandAction,
)


class FakeFileSystem(IFileSystem):
    """Fake file system."""

    def __init__(self) -> None:
        """Create new instance."""
        self._memory: list[FileSystemCommand] = []

    def copy(self, src: Path, dest: Path) -> None:
        """Copy file.

        Args:
            src (Path): source path.
            dest (Path): destination path.

        """
        self._memory.append(
            FileSystemCommand(
                command=FileSystemCommandAction.copy,
                source=src,
                destination=dest,
            )
        )

    def move(self, src: Path, dest: Path) -> None:
        """Move file.

        Args:
            src (Path): source path.
            dest (Path): destination path.

        """
        self._memory.append(
            FileSystemCommand(
                command=FileSystemCommandAction.move,
                source=src,
                destination=dest,
            )
        )

    def delete(self, src: Path, dest: Path | None = None) -> None:
        """Delete file.

        Args:
            src (Path): source path.
            dest (Path | None, optional): destination path. Defaults to None.

        """
        self._memory.append(
            FileSystemCommand(
                command=FileSystemCommandAction.delete,
                source=src,
                destination=dest,
            )
        )

    def history(self) -> list[FileSystemCommand]:
        """Get history.

        Returns:
            list[FileSystemCommand]: history.

        """
        return self._memory
