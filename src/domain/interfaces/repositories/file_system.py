"""File system repository interface."""

from pathlib import Path
from typing import Protocol

from src.domain.value_objects.file_system_command import FileSystemCommand


class IFileSystem(Protocol):
    """File system repository interface."""

    def copy(self, src: Path, dest: Path) -> None:
        """Copy file.

        Args:
            src (Path): source path.
            dest (Path): destination path.

        """
        ...

    def move(self, src: Path, dest: Path) -> None:
        """Move file.

        Args:
            src (Path): source path.
            dest (Path): destination path.

        """
        ...

    def delete(self, src: Path, dest: Path | None = None) -> None:
        """Delete file.

        Args:
            src (Path): source path.
            dest (Path | None, optional): destination path. Defaults to None.

        """
        ...

    def history(self) -> list[FileSystemCommand]:
        """Get history.

        Returns:
            list[FileSystemCommand]: history.

        """
        ...
