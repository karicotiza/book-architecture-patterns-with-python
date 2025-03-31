"""File system command value object."""

from dataclasses import dataclass
from pathlib import Path

from src.domain.value_objects.file_system_command_action import (
    FileSystemCommandAction,
)


@dataclass(slots=True, frozen=True)
class FileSystemCommand:
    """File system command value object."""

    command: FileSystemCommandAction
    source: Path
    destination: Path | None = None
