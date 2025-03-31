"""File system command action value object."""

from enum import StrEnum


class FileSystemCommandAction(StrEnum):
    """File system command action value object."""

    copy = "COPY"
    move = "MOVE"
    delete = "DELETE"
